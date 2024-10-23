from django.db import models
from users.models import User
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}
STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class Document(models.Model):
    file = models.FileField(
        upload_to='documents/',
        **NULLABLE
    )
    title = models.CharField(
        max_length=255,
        default='Документ',
        verbose_name='Название'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=STATUS,
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title or 'Unnamed Document'


class Notification(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Документ'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    message = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f"Notification for {self.document.title}"
