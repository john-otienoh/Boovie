from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('verify_otp/<uuid:user_id>/', views.verify_otp, name='verify_otp'),
    path('resend_otp/<uuid:user_id>/', views.resend_otp, name='resend_otp'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]