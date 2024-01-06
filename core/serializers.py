from rest_framework import serializers
from .models import Item, Order, Product, Cart


class ProductSerializer(serializers.ModelSerializer):
  price = serializers.FloatField(max_value=None, min_value=0)
  image = serializers.ImageField(max_length=None, use_url=True, required=False)
  
  class Meta:
    model = Product
    fields = '__all__'
        
class ItemSerializer(serializers.ModelSerializer):
  on_create_price = serializers.FloatField(required=False, max_value=None, min_value=0)
  
  class Meta:
    model = Item
    fields = '__all__'
    extra_kwargs = {'on_create_price': {'read_only': True}}
        
class OrderSerializer(serializers.ModelSerializer):
  items = ItemSerializer(many=True, read_only=True)
  
  class Meta:
    model = Order
    fields = ["id", "status", "customer", "items", "total", "created_at"]
    extra_kwargs = {'total': {'read_only': True}}
    
class CartSerializer(serializers.ModelSerializer):
  items = ItemSerializer(many=True, read_only=True)
  
  class Meta:
      model = Cart
      fields = ["id", "customer", "items", "total"]
      extra_kwargs = {'total': {'read_only': True}}
    