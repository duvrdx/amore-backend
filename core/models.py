from django.db import models
from users.models import SystemUser

class Base(models.Model):
  id = models.AutoField(primary_key=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    abstract = True

class Product(Base):
  CATEGORY_CHOICES = (
    ('anel', 'Anel'),
    ('brinco', 'Brinco'),
    ('colar', 'Colar'),
    ('pulseira', 'Pulseira'),
    ('pingente', 'Pingente'),
    ('alianca', 'Aliança'),
    ('relogio', 'Relógio'),
    ('outro', 'Outro')
  )
  
  SIZES_CHOICES = (
    ('pp', 'PP'),
    ('p', 'P'),
    ('m', 'M'),
    ('g', 'G'),
    ('gg', 'GG'),
    ('u', 'Único')
  )
  name = models.CharField(max_length=255)
  code = models.IntegerField(null=False, blank=False, unique=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField(null=True, blank=True)
  category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='outro')
  size = models.CharField(max_length=255, choices=SIZES_CHOICES, default='u')
  image = models.ImageField(upload_to='products')

  def __str__(self):
    return self.name
  
  def get_size_display(self):
        size_mapping = dict(self.SIZES_CHOICES)
        return size_mapping.get(self.size, self.size)
    
class Item(Base):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
  quantity = models.PositiveIntegerField(default=1)
  on_create_price = models.DecimalField(max_digits=5, decimal_places=2)
  
  
  def save(self, *args, **kwargs):
    self.on_create_price = self.product.price
    super().save(*args, **kwargs)

  @property
  def total(self):
    return self.product.price * self.quantity
    
class Order(Base):

  STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('canceled', 'Canceled'),
    ('done', 'Done'),
    ('delivering', 'Delivering')
  )

  status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='created')
  customer = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name='orders')
  items = models.ManyToManyField(Item, related_name='orders')
  
  @property
  def total(self):
    return sum(item.total for item in self.items.all())

    
  def __str__(self):
    return f'{self.customer.username} - {self.status} - {self.id}'
    
class Cart(Base):
  customer = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name='carts')
  items = models.ManyToManyField(Item, related_name='carts')
  
  def __str__(self):
    return f'{self.customer.username} - {self.created_at}'
    
  @property
  def total(self):
    return sum(item.total for item in self.items.all())
    
  def add_item(self, product_id, quantity=1):
    product = Product.objects.get(id=product_id)
    item, created = Item.objects.get_or_create(product=product, quantity=quantity)
    self.items.add(item)
    return item
    
  def remove_item(self, item_id):
    item = Item.objects.get(id=item_id)
    self.items.remove(item)
    return item
    
  def checkout(self):
    order = Order.objects.create(customer=self.customer)
    for item in self.items.all():
        order.items.add(item)

    order.save()
    self.items.clear()
    return order