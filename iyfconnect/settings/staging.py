from datetime import timedelta

from iyfconnect.settings.base import *


ALLOWED_HOSTS = ['backend-dev.iyfconnect.app','local.iyfconnect.app', '172.31.1.100']
DEBUG = True
ENVIRONMENT = env('ENVIRONMENT')
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=120),
}
CSRF_TRUSTED_ORIGINS = ['https://*.iyfconnect.app']
# extra static and media file settings.
AWS_STORAGE_BUCKET_NAME = 'iyfconnect-backend-dev'
AWS_S3_CUSTOM_DOMAIN = 'cdn-dev.iyfconnect.app'
# Static files (CSS, JavaScript, images)
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# Media files
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
CORS_ALLOW_ALL_ORIGINS = True



