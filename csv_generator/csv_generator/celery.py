import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_generator.settings')

app = Celery('csv_generator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')