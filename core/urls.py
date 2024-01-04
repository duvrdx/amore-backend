from django.urls import path
from .views import ProductViewSet, ItemViewSet, OrderViewSet, CartViewSet, CartCheckoutView, CartAddItemView

urlpatterns = [
  path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('products/<int:pk>', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
  path('items/', ItemViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('items/<int:pk>', ItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
  path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('orders/<int:pk>', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
  path('carts/', CartViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('carts/<int:pk>', CartViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
  path('carts/<int:pk>/checkout/', CartCheckoutView.as_view(), name='cart-checkout'),
  path('carts/<int:pk>/add/<int:product_id>', CartAddItemView.as_view(), name='cart-add'),
]
