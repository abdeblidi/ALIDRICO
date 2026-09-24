"""
Django settings for eleccatalog_project project.
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-change-this-in-production-eleccatalog-2026'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production-eleccatalog-2026')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# =========================================================
# Application definition
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'catalog',
    'dashboard',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'catalog.middleware.AdminEnglishMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'eleccatalog_project.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catalog.context_processors.categories',
            ],
        },
    },
]


WSGI_APPLICATION = 'eleccatalog_project.wsgi.application'


# =========================================================
# Database
# =========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================================================
# Password validation
# =========================================================

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


# =========================================================
# Internationalization
# =========================================================

# اللغة الافتراضية
LANGUAGE_CODE = 'ar'

# اللغات التي نريد دعمها
LANGUAGES = [
    ('ar', 'العربية'),
    ('fr', 'Français'),
    ('en', 'English'),
]

TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True
USE_TZ = True

# مجلد ملفات الترجمة
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# =========================================================
# Static files
# =========================================================

#STATIC_URL = 'static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# =========================================================
# Media files
# =========================================================


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =========================================================
# Default primary key field type
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'