from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pytz import all_timezones
from .models import UserProfile


class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com"]
        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError(f"Please use an email from the following domains: {', '.join(allowed_domains)}")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already registered. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Explicitly create or update the UserProfile (without timezone)
            UserProfile.objects.get_or_create(user=user)

        return user


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domains = [
            "gmail.com", "yahoo.com", "outlook.com", "icloud.com"
        ]

        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError(
                f"Please use an email from the following domains: {', '.join(allowed_domains)}"
            )

        return email

