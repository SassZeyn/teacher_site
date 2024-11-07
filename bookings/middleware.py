# In your Django app, create a new file: `middleware.py`
from django.shortcuts import redirect

class EmailVerificationRequiredMiddleware:
    """
    Middleware that redirects users who have not verified their email.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip checks for anonymous users
        if request.user.is_authenticated and not request.user.is_active:
            return redirect('email_verification_pending')
        return self.get_response(request)
