from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('verify_otp/<uuid:user_id>/', views.verify_otp, name='verify_otp'),
    path('resend_otp/<uuid:user_id>/', views.resend_otp, name='resend_otp'),
]