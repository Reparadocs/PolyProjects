"""
Django settings for PolyProjects project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Moved to secret.py
SECRET_KEY = os.environ.get('SECRET_KEY','test_key')

# SECURITY WARNING: don't run with debug turned on in production!
LOGIN_URL = '/login/'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'listings.UserProfile'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'listings'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'PolyProjects.urls'

WSGI_APPLICATION = 'PolyProjects.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.request',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'PolyProjectsDB',
        'USER': 'PolyProjectsUser',
        'PASSWORD': 'PolyProjectsPassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/listings/'

EMAIL_PORT = 25

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

