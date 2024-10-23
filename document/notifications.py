from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document
from .tasks import send_admin_notification


@receiver(post_save, sender=Document)
def notify_admin_on_document_submission(sender, instance, created, **kwargs):
    if created:
        send_admin_notification.delay(
            subject='Новый документ на рассмотрение',
            message=f'Документ "{instance.title}" был загружен пользователем {instance.user.username}.'
        )
