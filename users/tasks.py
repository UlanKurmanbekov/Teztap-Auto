from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_email_task(email, reset_link):

    send_mail(
        subject='Password Reset Request',
        message=f'Use this link to reset your password:\n\n{reset_link}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
