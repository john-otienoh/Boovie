import pyotp
from dotenv import load_dotenv
from django.conf import settings
from django.core.mail import send_mail

load_dotenv()

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    return totp.now()

def verify_otp(otp, user_otp):
    return otp == user_otp

def check_otp(submitted_otp, stored_otp):
    return str(submitted_otp).strip() == str(stored_otp).strip()

def send_otp(user):
    subject = '🔑 OTP Verification for Boovie'
    
    html_message = f"""
    <div style="max-width: 500px; margin: auto; font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #ddd;">
        <div style="text-align: center;">
            <h2 style="color: #333;">🎬 Boovie OTP Verification</h2>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px;">
            <p style="font-size: 16px; color: #555;">Hello,</p>
            <p style="font-size: 16px; color: #555;">Thank you for using <strong>FilmSphere</strong>. Your OTP code is:</p>
            <p style="font-size: 24px; font-weight: bold; color: #e74c3c; text-align: center; padding: 10px; background: #f2f2f2; border-radius: 8px;">{user.email_otp}</p>
            <p style="font-size: 14px; color: #888;">If you did not request this OTP, please ignore this email.</p>
        </div>
        <div style="text-align: center; margin-top: 20px; font-size: 14px; color: #777;">
            <p>Best regards,</p>
            <p><strong>The Boovie Team</strong></p>
        </div>
    </div>
    """
    
    send_mail(
        subject, 
        '',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message=html_message
    )

