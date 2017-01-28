"""
development settings, extends/overrides production settings
"""

from .production import *

DEBUG = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'server', 'dev', 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'server', 'dev', 'static')
AUTH_PASSWORD_VALIDATORS = []  # disable password policies
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
