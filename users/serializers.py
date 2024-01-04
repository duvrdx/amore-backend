from .models import SystemUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = SystemUser
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone',
              'password', 'house_number', 'zip_code']
    extra_kwargs = {
        'password': {
            'write_only': True,
            'style': {'input_type': 'password'}
        }
    }
  
  def create(self, validated_data):
    password = validated_data.pop('password', None)
    user = SystemUser(**validated_data)

    if password:
        user.set_password(password)

    user.save()
    return user
