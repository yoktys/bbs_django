# -*- coding: utf-8 -*-

from bbs.settings.base import *

DEBUG = False

VAR_ROOT = '/var/www/bbs'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

ROOT_URLCONF = 'bbs.urls.base'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'my_project_name',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
    }
}

# WSGI_APPLICATION = 'bbs.wsgi.production.application'
