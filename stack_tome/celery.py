import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stack_tome.settings')

app = Celery('stack_tome')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'Europe/Kiev'
