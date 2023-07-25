import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fundoo_notes.settings")
app = Celery("fundoo_notes")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
