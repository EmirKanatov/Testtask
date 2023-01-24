from .base import *

from .jazzmin import JAZZMIN_SETTINGS

DEBUG = False
ALLOWED_HOSTS = ['yourproject.example.com']

JAZZMIN_SETTINGS=JAZZMIN_SETTINGS

# Nado budet podcludhit postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}