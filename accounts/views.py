from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,  logout
from .forms import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages


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
    return render(request, 'register.html')

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
    return render(request, 'verify_otp.html', {'user': user})



def login_view(request):
    # if request.user.is_authenticated:
    #     messages.info(request, "You are already logged in.")
    #     return redirect('profile')
    
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

    return render(request, 'login.html', {'form': form})

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
    return render(request, "profile.html")

@login_required
def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

def home(request):
    return render(request, 'home.html')
