from django.urls import path
from .views import UserViewSet, get_user_data

urlpatterns = [
  path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('users/<int:pk>', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
  path('get_user_data/', get_user_data, name='get_user_data'),
]
