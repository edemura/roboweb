import os
from datetime import timedelta
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')

app = Celery('dtb')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.enable_utc = False

app.conf.beat_schedule = {
    "label_generate": {  # уникальное название задачи
        "task": 'users.tasks.label_generate',  # путь к задаче
        "schedule": timedelta(seconds=1),  # интервал, через который будет выполняться задача
    },
     "send_to_robo7": {  
        "task": 'users.tasks.send_to_robo7',  
        "schedule": timedelta(seconds=1), 
    },
     "check_robo7_complete": {  
        "task": 'users.tasks.check_robo7_complete',  
        "schedule": timedelta(seconds=1), 
    },
}    