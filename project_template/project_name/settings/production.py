"""
base settings, extended/overridden by dev settings when appropriate

https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
)))

INSTALLED_APPS = [
    'material',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'apps.registration',
    'apps.landing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]


# Domain & site configuration

SITE_NAME = '{{ project_name }}'
SITE_SCHEMA = os.environ.get('SCHEMA', 'http')
SITE_DOMAIN = os.environ.get('FQDN', 'localhost')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# URLs & static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

ROOT_URLCONF = '{{ project_name }}.urls'
MEDIA_ROOT = '/var/media/{{ project_name }}/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/var/media/{{ project_name }}/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '{{ project_name }}', 'static'),
)


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', '{{ project_name }}'),
        'USER': os.environ.get('DB_USER', '{{ project_name }}'),
        'PASSWORD': os.environ.get('DB_PASS', '{{ project_name }}'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Auth Configuration

AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'root'
LOGOUT_URL = 'logout'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
)
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# Email settings

class EmailSettings:
    HEADER_COLOR = "#03a9f4"  # Material Blue 500
    BG_COLOR = "#f5f5f5"  # Material Grey 100
    CONTENT_COLOR = "#ffffff"  # White
    HIGHLIGHT_COLOR = "#f5f5f5"  # Material Grey 100
    LOGO_URL = ("{schema}://{domain}{static_url}"
                "img/{{ project_name }}-logo.png").format(
        schema=SITE_SCHEMA, domain=SITE_DOMAIN, static_url=STATIC_URL)
    LOGO_ALT_TEXT = ""
    TERMS_URL = ""
    PRIVACY_URL = ""
    UNSUBSCRIBE_URL = ""
    FONT_CSS = ('font-family: "Helvetica Neue", "Helvetica", Helvetica, '
                'Arial, sans-serif;')
    FONT_CSS_HEADER = ('font-family: "HelveticaNeue-Light", '
                       '"Helvetica Neue Light", "Helvetica Neue", Helvetica, '
                       'Arial, "Lucida Grande", sans-serif;')
EMAIL = EmailSettings()
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_PORT = os.environ.get('EMAIL_HOST_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = bool(os.environ.get('EMAIL_USE_TLS'))
DEFAULT_FROM_EMAIL = 'no-reply@{}'.format(SITE_DOMAIN)
MANAGERS = ADMINS = (
    ('Administrator', 'admin@{}'.format(SITE_DOMAIN)),
)

INTERNAL_IPS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = [SITE_DOMAIN] + INTERNAL_IPS


# Logging
# The numeric values of logging levels are in the following table:
#
# CRITICAL    50
# ERROR       40
# WARNING     30
# INFO        20
# DEBUG       10
# NOTSET      0 [default]
#
# Messages which are less severe than the specified level will be ignored.
from django.utils.log import DEFAULT_LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': DEFAULT_LOGGING['filters'],
    'formatters': {
        'default': {
            '()': 'logging.Formatter',
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'debug': {
            '()': 'logging.Formatter',
            'format': '[%(asctime)s] %(levelname)s - %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_false'],
        },
        'debug-console': {
            'level': 'INFO',  # DEBUG level here is *extremely* noisy
            'class': 'logging.StreamHandler',
            'formatter': 'debug',
            'filters': ['require_debug_true'],
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': '/var/log/{{ project_name }}/django.log',
            'maxBytes': 1000000,  # 1MB
            'delay': True,
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'debug-console', 'file'],
            'level': 'NOTSET',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'debug-console', 'file'],
            'level': 'NOTSET',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'debug-console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# Caching
CACHES = {
    'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '{{ project_name }}', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                '{{ project_name }}.context_processors.site_name',
            ],
        },
    },
]


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# wsgi
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

USE_TZ = True
TIME_ZONE = 'America/Denver'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True


# bootstrap fix for message constants
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
