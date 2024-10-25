from django.contrib import admin
from .models import Document
from .tasks import send_user_notification


@admin.action(description='Одобрить выбранные документы')
def approve_document(modeladmin, request, queryset):
    """
    Действия для одобрения документов в админ-панели
    """
    queryset.update(status='approved')
    for document in queryset:
        send_user_notification.delay(document.user.email, 'подтвержден', document.title)


@admin.action(description='Отклонить выбранные документы')
def reject_document(modeladmin, request, queryset):
    """
    Действия для отклонения документов в админ-панели
    """
    queryset.update(status='rejected')
    for document in queryset:
        send_user_notification.delay(document.user.email, 'отклонен', document.title)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Регистрация модели Document в админ-панели с настройкой отображения и действиями
    """
    list_display = ['title', 'user', 'status', 'created_at']
    actions = [approve_document, reject_document]
