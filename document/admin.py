from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at']
    actions = ['approve_documents', 'reject_documents']

    def approve_documents(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, 'Выбранные документы были одобрены.')

    def reject_documents(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, 'Выбранные документы были отклонены.')

    approve_documents.short_description = 'Одобрить выбранные документы'
    reject_documents.short_description = 'Отклонить выбранные документы'
