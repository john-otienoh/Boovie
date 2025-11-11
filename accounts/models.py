import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True
    )
    username = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    is_email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    balance = models.IntegerField(default=1500)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username