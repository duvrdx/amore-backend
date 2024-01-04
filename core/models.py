from django.db import models
from users.models import SystemUser

class Base(models.Model):
  id = models.AutoField(primary_key=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    abstract = True

class Product(Base):
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  image = models.ImageField(upload_to='products')

  def __str__(self):
    return self.name
    
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
  costumer = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name='orders')
  items = models.ManyToManyField(Item, related_name='orders')
  
  @property
  def total(self):
    return sum(item.total for item in self.items.all())

    
  def __str__(self):
    return f'{self.costumer.username} - {self.status}'
    
class Cart(Base):
  costumer = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name='carts')
  items = models.ManyToManyField(Item, related_name='carts')
  
  def __str__(self):
    return f'{self.costumer.username} - {self.created_at}'
    
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
    order = Order.objects.create(costumer=self.costumer)
    for item in self.items.all():
        order.items.add(item)

    order.save()
    self.items.clear()
    return order