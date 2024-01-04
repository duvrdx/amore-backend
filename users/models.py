from django.db import models
from django.contrib.auth.models import AbstractUser

class SystemUser(AbstractUser):
  phone = models.CharField(max_length=11, blank=True, null=True)
  zip_code = models.CharField(max_length=255, null=True, blank=True)
  house_number = models.CharField(max_length=255, null=True, blank=True)
  