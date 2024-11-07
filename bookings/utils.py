from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as token_generator

def send_verification_email(user, request):
    """
    Send a verification email with a unique token to activate the user's account.
    """
    current_site = get_current_site(request)
    subject = "Activate Your Account"
    message = render_to_string('registration/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })
    send_mail(
        subject,
        message,
        'admin@example.com',  # Replace with your email
        [user.email],
        fail_silently=False,
    )
