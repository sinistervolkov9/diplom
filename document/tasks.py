from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_admin_notification(subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email for admin_email in settings.ADMINS]
        )
    except Exception as e:
        print(f'Ошибка при отправке уведомления: {e}')
