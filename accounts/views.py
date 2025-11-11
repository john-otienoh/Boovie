from django.shortcuts import render, redirect
from django.contrib.auth import login

from .utils import generate_otp, verify_otp, send_otp, check_otp
from .models import CustomUser

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = CustomUser.objects.create_user(
            username=username, email=email, password=password
        )
        email_otp = generate_otp()
        user.email_otp = email_otp
        user.save()

        send_otp(
            email=email, otp=email_otp
        )

        return redirect('verify_otp', user_id=user.id)
    return render(request, 'register.html')

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        email_otp = request.POST['email_otp']
        if check_otp(email_otp, user.email_otp):
            user.is_email_verified = True
            user.email_otp = None
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html')

def home(request):
    return render(request, 'home.html')
