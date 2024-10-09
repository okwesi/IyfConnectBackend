from pathlib import Path

from decouple import config as env
from kombu import Queue
from kombu.utils.url import safequote

from iyfconnect.celery_schedule import CELERY_BEAT_SCHEDULES, CELERY_TASK_ROUTES_QUEUES

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',

    # local apps
    'apps.accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iyfconnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'iyfconnect.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'ATOMIC_REQUESTS': True,

    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

APPEND_SLASH = False
# AWS S3 configuration
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = 'us-west-2'

aws_access_key = safequote(AWS_ACCESS_KEY_ID)
aws_secret_key = safequote(AWS_SECRET_ACCESS_KEY)

ENVIRONMENT = env('ENVIRONMENT')

STATIC_URL = 'static/'

# Static files (CSS, JavaScript, images)
STATICFILES_STORAGE = 'apps.shared.overrides.StaticRootS3Boto3Storage'

# Media files
DEFAULT_FILE_STORAGE = 'apps.shared.overrides.MediaRootS3Boto3Storage'

CORS_ALLOWED_ORIGINS = [
    'https://local.iyfconnect.com',
    'http://localhost:8000',
    'http://0.0.0.0:8000',
    'http://127.0.0.1:0000',
]

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [

        'rest_framework.throttling.AnonRateThrottle',

        'rest_framework.throttling.UserRateThrottle'

    ],
    'DEFAULT_THROTTLE_RATES': {

        'anon': '60/min',

        'user': '120/min'

    },
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'apps.shared.utils.renderer.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

}

CELERY_BROKER_URL = "sqs://{aws_access_key}:{aws_secret_key}@".format(
    aws_access_key=aws_access_key, aws_secret_key=aws_secret_key,
)

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_TRANSPORT_OPTIONS = {'region': 'us-west-2'}
CELERY_BEAT_SCHEDULE = CELERY_BEAT_SCHEDULES

CELERY_DEFAULT_QUEUE = ENVIRONMENT
CELERY_QUEUES = (
    Queue(ENVIRONMENT),
)
CELERY_TASK_ROUTES = CELERY_TASK_ROUTES_QUEUES
CELERY_MAX_RETRIES = 3
CELERY_DEFAULT_RETRY_DELAY = 10
