from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,  logout
from .forms import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .utils import generate_otp, send_otp, check_otp
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
        user.otp_created_at = timezone.now()
        user.last_otp_sent_at = timezone.now()
        user.save()

        send_otp(user)
        messages.info(request, "An OTP has been sent to your email.")
        return redirect('verify_otp', user_id=user.id)
    return render(request, 'accounts/register.html')

def verify_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        email_otp = request.POST['email_otp']

        if user.is_otp_expired():
            messages.warning(request, "Your OTP has expired. Please request a new one.")
            return redirect('verify_otp', user_id=user.id)
        
        if check_otp(email_otp, user.email_otp):
            user.is_email_verified = True
            user.email_otp = None
            user.otp_attempts = 0
            user.save()
            login(request, user)
            messages.success(request, "Email verified successfully!")
            return redirect('login')
        else:
            user.otp_attempts += 1
            user.save()
            messages.error(request, "Invalid OTP. Please try again.")

            # return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'accounts/verify_otp.html', {'user': user})



def login_view(request):
    if request.user.is_authenticated:
        # messages.info(request, "You are already logged in.")
        return redirect('profile')
    
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        email = request.POST.get('username')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0) 
            else:
                request.session.set_expiry(60 * 60 * 24 * 7)

            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or reverse('profile')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid Username or password")
    else:
        form = EmailAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def resend_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if not user.can_send_otp():
        messages.warning(request, "Please wait 1 minute before requesting another OTP.")
        return redirect('verify_otp', user_id=user.id)

    emaail_otp = generate_otp()
    user.email_otp = emaail_otp
    user.otp_created_at = timezone.now()
    user.last_otp_sent_at = timezone.now()
    user.save()
    send_otp(user)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_otp', user_id=user.id)

@login_required
def profile(request):
    return render(request, "accounts/profile.html")

@login_required
def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        
        if not user:
            messages.error(request, "No account with that email found")
            return redirect('forgot-password')
        
        if hasattr(user, 'is_email_verified') and not user.is_email_verified:
            messages.error(request, 'Please verify your email before resetting your password.')
            return redirect('forgot_password')

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(f'/account/reset-password/{uid}/{token}/')

        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'Password reset link sent to your email.')
        return redirect('login')
    return render(request, "accounts/forgot_password.html")


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                user.set_password(password)
                user.save()
                messages.success(request, "'Password reset successful. You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'accounts/reset_password.html')
    else:
        messages.error(request, "Invalid or expired reset link")
        return redirect('forgot_password')
    
