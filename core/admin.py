from django.contrib import admin

from .models import Product, Item, Order, Cart

admin.site.register(Product)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Cart)


