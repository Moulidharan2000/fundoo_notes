from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notes
from .tasks import send_mail


@receiver(post_save, sender=Notes)
def save_note(sender, instance, **kwargs):
    if instance.user.email:
        send_mail.delay(instance.user.email)


