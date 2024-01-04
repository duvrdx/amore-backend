from rest_framework import viewsets
from .models import Item, Order, Product, Cart
from .serializers import ItemSerializer, OrderSerializer, ProductSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .utils import get_resume, send_order_to_admin, send_order_to_costumer

class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  
class ItemViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]
  queryset = Item.objects.all()
  serializer_class = ItemSerializer
  
class OrderViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
  
class CartViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]
  queryset = Cart.objects.all()
  serializer_class = CartSerializer

class CartCheckoutView(generics.UpdateAPIView):
  queryset = Cart.objects.all()
  serializer_class = CartSerializer

  def update(self, request, *args, **kwargs):
    cart = self.get_object()
    order = cart.checkout()
    
    try:
      order_resume = get_resume(order)
      send_order_to_costumer(cart, order_resume)
      send_order_to_admin(cart, order_resume)
            
    except Exception as e:
      print(e)
      return Response({'error': 'Erro ao enviar e-mail.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = self.get_serializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

class CartAddItemView(generics.UpdateAPIView):
  queryset = Cart.objects.all()
  serializer_class = CartSerializer

  def update(self, request, *args, **kwargs):
    cart = self.get_object()
    product_id = kwargs.get('product_id')

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Produto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    cart.add_item(product.id)

    serializer = self.get_serializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)