from .base import *

from .jazzmin import JAZZMIN_SETTINGS

DEBUG = False
ALLOWED_HOSTS = ['yourproject.example.com']

JAZZMIN_SETTINGS=JAZZMIN_SETTINGS

# Nado budet podcludhit postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("SQL_NAME"),
        'PASSWORD': env("SQL_PASSWORD"),
        'USER': env("SQL_USER"),
        'HOST': env("SQL_HOST"),
        'PORT': '5432'
    }
}