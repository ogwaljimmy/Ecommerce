
import os
from dotenv import load_dotenv
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-olc_l4v9uimldmd)xjf0qcgbl#f3zyln(b##@b26_&2q_oo@_d'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['*']

#CSRF_TRUSTED_ORIGINS = ['']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store', # Django app
    'cart', # Django app
    'account', # Django app
    'payment', # Django app
    'mathfilters',
    'crispy_forms', # Crispy forms
    'storages',
    'pwa',

]

# To un-block PayPal popups - NB!

SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'


# Crispy forms

CRISPY_TEMPLATE_PACK = 'bootstrap4'


MIDDLEWARE = [ 

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.views.categories', # Updated
                'cart.context_processors.cart',

            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'static/media'



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



PWA_APP_NAME = 'Edenthought'
PWA_APP_SHORT_NAME = 'Edenthought'
PWA_APP_DESCRIPTION = "Premium Digital Marketplace"
PWA_APP_THEME_COLOR = '#2c3e50'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/images/favicon.ico',
        'sizes': '64x64',
        'type': 'image/x-icon'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/favicon.ico',
        'sizes': '64x64'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

# Email configuration settings:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = 'True'

# Be sure to read the guide in the resources folder of this lecture (SETUP THE EMAIL BACKEND)

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


# PayPal Configuration
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET_KEY = os.getenv('PAYPAL_SECRET_KEY')
PAYPAL_ENVIRONMENT = os.getenv('PAYPAL_ENVIRONMENT', 'sandbox')  # Default to sandbox

# Payment Gateway Settings
# Flutterwave Payment Gateway
FLUTTERWAVE_PUBLIC_KEY = config('FLUTTERWAVE_PUBLIC_KEY')
FLUTTERWAVE_SECRET_KEY = config('FLUTTERWAVE_SECRET_KEY')
FLUTTERWAVE_ENCRYPTION_KEY = config('FLUTTERWAVE_ENCRYPTION_KEY')
BASE_URL = config('BASE_URL', default='http://localhost:8000')


# AWS configuration

'''
AWS_ACCESS_KEY_ID = '' # - Enter your AWS ACCESS KEY ID HERE
AWS_SECRET_ACCESS_KEY = '' # - Enter your AWS SECRET ACCESS KEY HERE


# Amazon S3 Integration

AWS_STORAGE_BUCKET_NAME = '' # - Enter your S3 bucket name HERE

# Django 4.2 > Storage configuration for S3

STORAGES = {
    
    # Media file (image) management

    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    
    # CSS and JS file management

    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        
    },
    
}


AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False

'''


'''
# RDS (Database) configuration settings:
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': '', # Enter your Database name HERE

        'USER': '', # Enter your Database username HERE

        'PASSWORD': '', # Enter your Database password HERE

        'HOST': '', # Enter your Database host/endpoint HERE

        'PORT': '5432',
    }
}
'''






