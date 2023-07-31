from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notes
from .tasks import send_mail
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json


@receiver(post_save, sender=Notes)
def save_note(sender, instance, **kwargs):
    if instance.remainder:
        date = datetime.date(instance.remainder)
        day = date.day
        month = date.month
        year = date.year
        time = datetime.time(instance.remainder)
        hour = time.hour
        minutes = time.minute
        crontab, created = CrontabSchedule.objects.get_or_create(minute=minutes, hour=hour, day_of_month=day,
                                                                 month_of_year=month)
        task = PeriodicTask.objects.filter(name=f'{instance.user.id}-{instance.id}')
        if task.exists():
            task = task.first()
            task.crontab = crontab
            task.save()
        else:
            task = PeriodicTask.objects.create(crontab=crontab,
                                               name=f'{instance.user.id}-{instance.id}',
                                               task='notes.tasks.send_mail',
                                               args=json.dumps([instance.user.email, instance.title]))



# celery -A fundoo_notes worker -l info --pool=solo
# celery -A fundoo_notes beat -l info