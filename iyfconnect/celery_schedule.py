import os
from datetime import timedelta

from celery.schedules import crontab


queue = os.environ['ENVIRONMENT']

CELERY_BEAT_SCHEDULES = {

}

CELERY_TASK_ROUTES_QUEUES = {
    '*': {'queue': queue}
}
