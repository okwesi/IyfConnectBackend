from datetime import timedelta

from iyfconnect.settings.base import *

ALLOWED_HOSTS = [
    '172.31.10.233','iyfconnect.ngrok.app',
    'local.iyfconnect.app','backend.iyfconnect.app',
    '0.0.0.0'
]

DEBUG = False

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=120),
}

INTERNAL_HOST = env('INTERNAL_HOST')
CSRF_TRUSTED_ORIGINS = ['https://*.iyfconnect.app']
# extra static and media file settings.
AWS_STORAGE_BUCKET_NAME = 'iyfconnect-backend-live'
AWS_S3_CUSTOM_DOMAIN = 'cdn.iyfconnect.app'
# Static files (CSS, JavaScript, images)
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# Media files
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
CORS_ALLOW_ALL_ORIGINS = True
