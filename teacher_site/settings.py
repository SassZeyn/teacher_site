import os
from pathlib import Path
from django.contrib.messages import constants as messages
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

# Use BASE_DIR to locate .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Debug print
print("Loaded EMAIL_HOST_USER:", env("EMAIL_HOST_USER"))


# Message tag settings for Django messages framework
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

PAYPAL_CLIENT_ID = 'YOUR_PAYPAL_CLIENT_ID'
PAYPAL_CLIENT_SECRET = 'YOUR_PAYPAL_CLIENT_SECRET'
PAYPAL_MODE = 'sandbox'  # Use 'live' for production


AMERIA_MERCHANT_ID = 'your_merchant_id'
AMERIA_API_KEY = 'your_api_key'
AMERIA_ENDPOINT = 'https://payments.ameriabank.am/'  # Adjust based on their provided endpoint



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # keep False since you're using TLS
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default="")
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default=None)
DEFAULT_FROM_EMAIL = 'sasszeyn@gmail.com'


# Base directory path for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings (keep the secret key safe)

SECRET_KEY = env('SECRET_KEY')

# Debugging (set to False in production)
DEBUG = env.bool('DEBUG', default=False)


# Login and Logout configurations
LOGIN_URL = 'login'  # Route name for the login page
LOGOUT_REDIRECT_URL = 'homepage'  # Redirect to homepage after logout
LOGIN_REDIRECT_URL = 'homepage'  # Redirect to homepage after login

# Allowed hosts for the application
ALLOWED_HOSTS = ['sasszeyn.com', 'www.sasszeyn.com', '165.227.170.154']

# Static files configuration (CSS, JS, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'bookings', 'static')]  # Your static directory
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Where `collectstatic` will place static files

# Media files configuration (uploaded images and files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookings',  # Your custom app
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'bookings.middleware.EmailVerificationRequiredMiddleware',
]

ROOT_URLCONF = 'teacher_site.urls'


# Templates settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Path to your custom templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path
WSGI_APPLICATION = 'teacher_site.wsgi.application'

# Database configuration (using SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost'
        'PORT' '3306'
    }
}

# Password validation (Django's built-in validators)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


