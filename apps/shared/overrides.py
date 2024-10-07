import os

from django.utils import timezone
from django.utils.deconstruct import deconstructible

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
