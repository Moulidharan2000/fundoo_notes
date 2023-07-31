from celery import shared_task
from django.core.mail import send_mail as sm
from django.conf import settings


@shared_task()
def send_mail(recipient):
    sm(subject="mail send", message="fundoo notes", from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient])
    return "Mail Sent Successfully"
