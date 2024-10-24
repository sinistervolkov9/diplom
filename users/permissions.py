from rest_framework import permissions
from django.conf import settings


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет изменять/удалять документы только администраторам из settings.ADMINS.
    Обычные пользователи могут только просматривать свои документы или одобренные администрацией.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.is_admin(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.status == 'approved' or obj.user == request.user
        return self.is_admin(request.user)

    def is_admin(self, user):
        if user.is_staff:
            admin_emails = [email for _, email in settings.ADMINS]
            return user.email in admin_emails
        return False
