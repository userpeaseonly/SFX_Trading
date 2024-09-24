import os

from .defaults import * # noqa


DEBUG = True
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')


