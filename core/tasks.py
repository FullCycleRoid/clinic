from celery.task import periodic_task
from datetime import timedelta
from clinic2.celery import app
from .models import Appointment, MyModel



@periodic_task(run_every=timedelta(seconds=5))
def scan_appointment():
    appointment = Appointment.objects.filter(date='2020-03-02 11:00:00+00:00')
    print('-' * 100)
    print('Cronjob', appointment)

@periodic_task(run_every=timedelta(seconds=10))
def add_to_db():
    sometext = 'sdcsdfvadfvdfvadv'
    MyModel.objects.create(
        text=sometext
    )
    return 'Text added model created'


@app.task
def add(x, y):
    return x + y

