from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('verify_otp/<uuid:user_id>/', views.verify_otp, name='verify_otp'),
]