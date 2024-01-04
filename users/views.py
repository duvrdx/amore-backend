from rest_framework import viewsets
from .models import SystemUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from oauth2_provider.models import AccessToken

def get_user_data(request):
    try:
        access_token_value = request.GET.get('access_token')
        access_token = AccessToken.objects.get(token=access_token_value)
        user_data = {
            'id': access_token.user.id,
            'username': access_token.user.username,
            'email': access_token.user.email,
            'phone': access_token.user.phone,
        }
        return JsonResponse(user_data)
    except AccessToken.DoesNotExist:
        return JsonResponse({'error': 'Token inválido ou não encontrado'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = SystemUser.objects.all()
    serializer_class = UserSerializer
