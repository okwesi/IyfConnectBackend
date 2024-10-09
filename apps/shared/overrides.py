import os

from django.utils import timezone
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage


@deconstructible
class FileNameEngine:
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        # Get the current date and time
        current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')

        # Combine the instance id, date, and time to create the filename
        filename = f'{instance.id}_{current_datetime}.{ext}'

        # Return the whole path to the file
        return os.path.join(self.path, filename)
    
class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = 'static'  # This will store static files in a folder named 'static'
    default_acl = None


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    default_acl = None
