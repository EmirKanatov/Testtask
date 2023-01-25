import os

from .base import *
from .jazzmin import JAZZMIN_SETTINGS

DEBUG = True

JAZZMIN_SETTINGS=JAZZMIN_SETTINGS
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_DB"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'USER': env("POSTGRES_USER"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': '5432',
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')