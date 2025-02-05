import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]

SECRET_KEY = os.getenv("DJANGO_KEY", "some_key")

DEBUG = os.getenv("DEBUG_KEY", False) in ("True", "true", "TRUE", "1")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split()
DOCKER_CONTAINER_NAME = os.getenv("DOCKER_CONTAINER_NAME")
DOMAIN = os.getenv("DOMAIN")
SERVER_IP = os.getenv("SERVER_IP")
ALLOWED_HOSTS.extend([DOCKER_CONTAINER_NAME, DOMAIN, SERVER_IP])

CSRF_TRUSTED_ORIGINS = [
    f"https://{DOMAIN}",
]

"""default packeges"""
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

]

"""packages"""
INSTALLED_APPS += [
    "rest_framework",
    "rest_framework.authtoken",
    "social_django",
    "djoser",
    "drf_spectacular",
    "import_export",
    "corsheaders",
    "oauth2_provider",
    "drf_social_oauth2",
]

"""apps"""
INSTALLED_APPS += [
    "furniture",
    "users",
    "api",
    "tariff",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    f"https://{DOMAIN}",
]
CORS_ALLOW_ALL_HEADERS = True
CORS_ALLOW_CREDENTIALS = True
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "config.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", default="5433"),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "users.validators.password_validators.LengthValidator",
        "OPTIONS": {
            "max_length": 40,
        },
    },
    {
        "NAME": "users.validators.password_validators.SpecialCharsValidator",
    },
    {
        "NAME": "users.validators.password_validators.AllowedCharsValidator",
    },
    {
        "NAME": "users.validators.password_validators.HasUpperAndLowerCaseValidator",
    },
    {
        "NAME": "users.validators.password_validators.HasDigitValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "drf_social_oauth2.authentication.SocialAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # TODO: настроить троттлинг
    # "throttle_scope": [
    #     "rest_framework.throttling.UserRateThrottle",
    #     "rest_framework.throttling.AnonRateThrottle",
    #     "rest_framework.throttling.ScopedRateThrottle",
    #     "users.throttling.SustainedRateThrottle",
    # ],
    # "DEFAULT_THROTTLE_RATES": {
    #     "anon": "2/second",  # Лимит для AnonRateThrottle
    #     "user": "5/second",
    #     "long_time": "10/minute",
    # },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Dizi-izi API",
    "DESCRIPTION": "Документация для проекта Dizi-izi-backend",
    "VERSION": "v1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "CONTACT": {"email": "dizi.izi.plan@gmail.com"},
    "LICENSE": {"name": "MIT License"},
}

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "LOGIN_FIELD": "email",
    "PASSWORD_RESET_CONFIRM_URL": "reset-password/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "reset-username/{uid}/{token}",
    "EMAIL": {
        "activation": "users.emails.CustomActivationEmail",
        "password_reset": "users.emails.CustomPasswordResetEmail",
    },
}

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.yandex.YandexOAuth2",
    "drf_social_oauth2.backends.DjangoOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# Social auth keys
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET")
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_YANDEX_OAUTH2_KEY")
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_YANDEX_OAUTH2_SECRET")

# Settings MinIO S3
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("S3_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
AWS_S3_FILE_OVERWRITE = os.getenv("S3_FILE_OVERWRITE", False) in ("True", "true", "TRUE", "1")
AWS_QUERYSTRING_AUTH = os.getenv("S3_QUERYSTRING_AUTH", False) in ("True", "true", "TRUE", "1")

# константы проекта, если их будет много, то нужно будет их организовать в отдельном файле с разбивкой по тематике
MAX_LENGTH_PROJECT_NAME = 128
MAX_LENGTH_ROOM_NAME = 128
MAX_LENGTH_FURNITURE_NAME = 128
PROJECT_NAME_BY_DEFAULT = "Проект"
