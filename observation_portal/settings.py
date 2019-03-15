"""
Django settings for observation_portal project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2xou30pi2va&ed@n2l79n807k%@szj1+^uj&)y09_w62eji!m^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['observation-portal-dev.lco.gtn']

SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 7

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'registration',  # must come before admin to use custom templates
    'django.contrib.admin',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'rest_framework.authtoken',
    # 'silk',
    'bootstrap3',
    'oauth2_provider',
    'django_extensions',
    'observation_portal.accounts',
    'observation_portal.requestgroups',
    'observation_portal.observations',
    'observation_portal.proposals',
    'observation_portal.sciapplications',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SILKY_PYTHON_PROFILER = True
# SILKY_PYTHON_PROFILER_BINARY = True


ROOT_URLCONF = 'observation_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'observation_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
       'NAME': os.getenv('DB_NAME', 'observation_portal'),
       'USER': os.getenv('DB_USER', 'postgres'),
       'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
       'HOST': os.getenv('DB_HOST', 'localhost'),
       'PORT': os.getenv('DB_PORT', '5432')
   }
}

CACHES = {
     'default': {
         'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
         'LOCATION': os.getenv('CACHE_LOCATION', 'unique-snowflake')
     },
     'locmem': {
         'BACKEND': os.getenv('LOCAL_CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
         'LOCATION': 'locmem-cache'
     }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'observation_portal.accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
]

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 86400 * 30,  # 30 days
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400 * 30  # 30 days
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$|^/o/.*'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', 'observe.lco.global')
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
AWS_S3_CUSTOM_DOMAIN = 's3-us-west-2.amazonaws.com/{}'.format(AWS_STORAGE_BUCKET_NAME)
AWS_IS_GZIPPED = True
AWS_DEFAULT_ACL = None

STATICFILES_DIR = 'static'
STATIC_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, STATICFILES_DIR) if AWS_ACCESS_KEY_ID else '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '_static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = os.getenv('STATIC_STORAGE', 'django.contrib.staticfiles.storage.StaticFilesStorage')
MEDIAFILES_DIR = 'media'
MEDIA_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_DIR) if AWS_ACCESS_KEY_ID else '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = os.getenv('MEDIA_STORAGE', 'django.core.files.storage.FileSystemStorage')

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
DEFAULT_FROM_EMAIL = 'Webmaster <portal@lco.global>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'http://elasticsearchdev.lco.gtn')
CONFIGDB_URL = os.getenv('CONFIGDB_URL', 'http://configdbdev.lco.gtn')
DOWNTIMEDB_URL = os.getenv('DOWNTIMEDB_URL', 'http://downtimedb.lco.gtn')

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': (
        'observation_portal.accounts.throttling.AllowStaffUserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': '5000/day',
        'requestgroups.cancel': '1000/day',
        'requestgroups.create': '2500/day',
        'requestgroups.validate': '10000/day'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'rise_set': {
            'level': 'WARNING'
        },
        'valhalla_request': {
            'level': 'INFO',
            'propogate': False
        }
    }
}

CELERY_TASK_ALWAYS_EAGER = not os.getenv('CELERY_ENABLED', False)
CELERY_BROKER_URL = os.getenv('BROKER_URL', 'memory://localhost')
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

CELERY_BEAT_SCHEDULE = {
    'time-accounting-every-hour': {
        'task': 'observation_portal.proposals.tasks.run_accounting',
        'schedule': 3600.0
    },
    'expire-requests-every-5-minutes': {
        'task': 'observation_portal.userrequests.tasks.expire_requests',
        'schedule': 300.0
    },
    'expire-access-tokens-every-day': {
        'task': 'observation_portal.accounts.tasks.expire_access_tokens',
        'schedule': 86400.0
    }
}

TEST_RUNNER = 'observation_portal.test_runner.MyDiscoverRunner'

try:
    from local_settings import *  # noqa
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS  # noqa
    ALLOWED_HOSTS += LOCAL_ALLOWED_HOSTS  # noqa
except NameError:
    pass
