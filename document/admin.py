from django.contrib import admin
from .models import Document
from .tasks import send_user_notification


@admin.action(description='Одобрить выбранные документы')
def approve_document(modeladmin, request, queryset):
    """
    Действия для одобрения документов в админ-панели
    """
    for document in queryset:
        document.status = 'approved'
        document.save()
        send_user_notification.delay(document.user.email, 'подтвержден', document.title)


@admin.action(description='Отклонить выбранные документы')
def reject_document(modeladmin, request, queryset):
    """
    Действия для отклонения документов в админ-панели
    """
    for document in queryset:
        document.status = 'rejected'
        document.save()
        send_user_notification.delay(document.user.email, 'отклонен', document.title)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Регистрация модели Document в админ-панели с настройкой отображения и действиями
    """
    list_display = ['title', 'user', 'status', 'created_at']
    actions = [approve_document, reject_document]

    def save_model(self, request, obj, form, change):
        """
        Метод, который вызывается при сохранении модели.
        Отправляем уведомление пользователю, если статус документа изменен.
        """
        if change:
            old_status = Document.objects.get(pk=obj.pk).status
            if old_status != obj.status:
                send_user_notification.delay(obj.user.email, obj.status, obj.title)

        super().save_model(request, obj, form, change)
