from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notes
from .tasks import sample_task


@receiver(post_save, sender=Notes)
def save_note(sender, instance, **kwargs):
    sample_task.delay()


