"""
Django settings for Aldempro project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import django_heroku
import dj_database_url
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from django.utils.translation import gettext_lazy as _


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-op)%sbz31qyw_$-s1fia=af(4ipl@vpjl+6-eo54vnt&v!qz10'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'markdownx',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Aldemapp',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_select2',
    'widget_tweaks',
    'django_user_agents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'Aldemapp.middleware.BlockChangeAfterFirstLoginMiddleware',


]


CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/']

SECURE_FRAME_DENY = True
X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'Aldempro.urls'
WSGI_APPLICATION = 'Aldempro.wsgi.application'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'Aldempro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuwait'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

django_heroku.settings(locals())

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOGIN_REDIRECT_URL = 'student'
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = '/'

LANGUAGES = [
    ('ar', _('Arabic')),
    # Add other languages here if needed
]

# Set the default language to Arabic
LANGUAGE_CODE = 'ar'

# Path to the locale directory
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


JAZZMIN_SETTINGS = {
    'welcome_sign': 'أهلاً وسهلاً في إدارة موقع الأستاذة الدمرداش',
    # 'show_sidebar': True,
    "login_logo":'assets/img/logo/logo.jpg'
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Replace with your preferred backend

EMAIL_PORT = 587  # Replace with your email port
EMAIL_USE_TLS = True  # Set to False if your email server doesn't use TLS
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your email host for gmail -> 'smtp.gmail.com'
EMAIL_HOST_USER = 'mtsmy31@gmail.com'  # Replace with your email username
EMAIL_HOST_PASSWORD = 'iqxc pbbq sxdr nzcs'  # Replace with your email password
DEFAULT_FROM_EMAIL = 'mtsmy31@gmail.com' 

