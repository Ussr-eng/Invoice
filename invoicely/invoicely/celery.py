import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoicely.settings')
app = Celery('invoicely')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'edit_consignment_note_500s': {
        'task': 'apps.order.tasks.edit_consignment_note',
        'schedule': 500.0
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
