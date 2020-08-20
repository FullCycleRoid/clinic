from celery.task import periodic_task
from datetime import timedelta
from .models import Appointment, MyModel
import datetime



@periodic_task(run_every=timedelta(seconds=2))
def scan_appointment():
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    appointment = Appointment.objects.filter(date__gte=date)
    print('-' * 100)
    print('Cronjob', appointment)

@periodic_task(run_every=timedelta(seconds=2))
def add_to_db():
    sometext = 'sdcsdfvadfvdfvadv'
    MyModel.objects.create(
        text=sometext
    )
    print('Text added model created')

@periodic_task(run_every=timedelta(seconds=2))
def add(x, y):
    return x + y

