import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic2.settings')
app = Celery('clinic2', backend='amqp', broker='amqp://guest@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()