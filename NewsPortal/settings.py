"""
Django settings for NewsPortal project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'news.apps.NewsConfig',
    'django_extensions',
    'django_filters',
    'crispy_forms',
    'django_apscheduler',
    'ckeditor',
    'ckeditor_uploader',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'news.middlewares.TimezoneMiddleware',
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates', 'allauth')]
        ,
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

WSGI_APPLICATION = 'NewsPortal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console_DEBUG_log': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'console_WARNING_log': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
        'console_ERROR_CRITICAL_log': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'style': '{',
        },
        'general_log': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'errors_log': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'style': '{',
        },
        'security_log': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'mail_admins': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        }
    },

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    'handlers': {
        'console_DEBUG': {
            'level': 'DEBUG',
            'formatter': 'console_DEBUG_log',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        },
        'console_WARNING': {
            'level': 'WARNING',
            'formatter': 'console_WARNING_log',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        },
        'console_ERROR_CRITICAL': {
            'level': 'ERROR',  # 'CRITICAL'
            'formatter': 'console_ERROR_CRITICAL_log',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'formatter': 'mail_admins',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'general_log': {
            'level': 'INFO',
            'filename': BASE_DIR/'logging/general.log',
            'formatter': 'general_log',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_false'],
        },
        'errors_log': {
            'level': 'ERROR',  # 'CRITICAL'
            'filename': BASE_DIR/'logging/errors.log',
            'formatter': 'errors_log',
            'class': 'logging.FileHandler',
        },
        'security_log': {
            'filename': BASE_DIR/'logging/security.log',
            'formatter': 'security_log',
            'class': 'logging.FileHandler',
        }
    },

    'loggers': {
        'django': {
            'handlers': ['console_DEBUG', 'console_WARNING', 'console_ERROR_CRITICAL', 'general_log'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errors_log', 'mail_admins'],
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_log'],
            'propagate': False,
        },
        'django.server': {
            'handlers': ['errors_log', 'mail_admins'],
            'propagate': False,
        },
        'django.template': {
            'handlers': ['errors_log'],
            'propagate': False,
        },
        'django.db_backends': {
            'handlers': ['errors_log'],
            'propagate': False,
        },
    },
}

ADMINS = [('admin', os.getenv('DEFAULT_FROM_EMAIL')), ]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Localization
LOCALE_PATH = [
    os.path.join(BASE_DIR, 'locale')
]


LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BAD_WORDS = os.path.join(BASE_DIR, "BAD_WORDS.txt")

CRISPY_FAIL_SILENTLY = not DEBUG

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/news/'
LOGOUT_REDIRECT_URL = '/news/'

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_FORMS = {'signup': 'news.forms.CommonSignupForm'}
# ACCOUNT_SIGNUP_FORM_CLASS = 'news.forms.LocalSignupForm' # TODO make self adding to "common" group through Google

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# REDIS_CREDENTIALS in format- redis://:password@hostname:port/db_number
# db_number = 0 (индекс БД)
CELERY_BROKER_URL = os.getenv('REDIS_CREDENTIALS', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_CREDENTIALS', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_TIME_LIMIT = 10

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
        ]),
    }
}

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
