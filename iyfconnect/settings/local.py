from datetime import timedelta

from iyfconnect.settings.base import *

DEBUG = env('DEBUG', cast=bool)
# ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='*', cast=Csv())
ALLOWED_HOSTS = ['local.iyfconnect.app','iyfconnect.ngrok.app','0.0.0.0']
ENVIRONMENT = env('ENVIRONMENT')
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=120),
}
CSRF_TRUSTED_ORIGINS = ['https://local.iyfconnect.app']

# extra static and media file settings.
AWS_STORAGE_BUCKET_NAME = 'iyfconnect-backend-local'
AWS_S3_CUSTOM_DOMAIN = 'cdn-local.iyfconnect.app'
# Static files (CSS, JavaScript, images)
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# Media files
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')