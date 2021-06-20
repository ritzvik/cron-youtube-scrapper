"""
Django settings for code_service project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from dotenv import load_dotenv
from celery.schedules import crontab
import os
import yaml

config_file = os.environ.get("APP_SECRET_FILE_PATH")

if not config_file:
    config_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "config",
        "app_secrets",
        "common_settings.yml",
    )

stream = open(config_file, "r")

try:
    APP_SECRETS = yaml.safe_load(stream)
finally:
    stream.close()

ENVIRONMENT = APP_SECRETS.get("ENVIRONMENT", "dev")

load_dotenv(verbose=True)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = APP_SECRETS["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = APP_SECRETS["DEBUG"]

ALLOWED_HOSTS = ["*"]
# cors settings
CORS_ALLOW_HEADERS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "django_celery_results",
    "django_celery_beat",
    "scrapper",
]

MIDDLEWARE = [
    "code_service.middleware.logger_middleware.RequestIdMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "code_service.middleware.exception_middleware.ExceptionMiddleware",
]

ROOT_URLCONF = "code_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "code_service.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": APP_SECRETS["databases"]["DB_NAME"],
        "USER": APP_SECRETS["databases"]["DB_USER"],
        "PASSWORD": APP_SECRETS["databases"]["DB_PASSWORD"],
        "HOST": APP_SECRETS["databases"]["DB_HOST"],
        "PORT": APP_SECRETS["databases"]["DB_PORT"],
        "CONN_MAX_AGE": (
            None
            if APP_SECRETS["databases"]["CONN_AGE"] < 0
            else APP_SECRETS["databases"]["CONN_AGE"]
        )  # Use negative value for `None` CONN_AGE in env
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REDIS_HOST = APP_SECRETS["redis"]["host"]
REDIS_PORT = APP_SECRETS["redis"]["port"]


CACHES = {
    "default": {
        "BACKEND": APP_SECRETS["caches"]["backend"],
        "LOCATION": "redis://%s:%s/0" % (REDIS_HOST, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": APP_SECRETS["caches"]["options"]["client_class"],
            "IGNORE_EXCEPTIONS": APP_SECRETS["caches"]["options"]["ignore_exceptions"],
            "PARSER_CLASS": APP_SECRETS["caches"]["options"]["parser_class"],
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# for persistent connection with DB
# https://docs.djangoproject.com/en/3.1/ref/databases/#persistent-connections
CONN_MAX_AGE = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
APPEND_SLASH = True
CACHE_PREFIX = APP_SECRETS["cache_prefix"]

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "queue_name_prefix": f"code_service-{ENVIRONMENT}-",
    "visibility_timeout": 3600,
}

CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "scrapper.tasks.populate_youtube_data_helper",
        "schedule": crontab(minute='*/1'), # every 1 minute
    }
}
