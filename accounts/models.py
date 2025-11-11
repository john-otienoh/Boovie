import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta

# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True
    )
    username = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    is_email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    last_otp_sent_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    balance = models.IntegerField(default=1500)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def can_send_otp(self):
        if not self.last_otp_sent_at:
            return True
        return (timezone.now() - self.last_otp_sent_at) > timedelta(seconds=60)

    def is_otp_expired(self):
        if not self.otp_created_at:
            return True
        return (timezone.now() - self.otp_created_at) > timedelta(minutes=2)