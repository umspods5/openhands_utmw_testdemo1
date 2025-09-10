import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlocker.settings')

app = Celery('smartlocker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'process-whatsapp-responses': {
        'task': 'notifications.tasks.process_whatsapp_responses',
        'schedule': 60.0,  # Every minute
    },
    'cleanup-expired-sessions': {
        'task': 'notifications.tasks.cleanup_expired_sessions',
        'schedule': 3600.0,  # Every hour
    },
}

app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')