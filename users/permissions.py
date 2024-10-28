from rest_framework import permissions
from django.conf import settings


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет изменять/удалять документы только администраторам из settings.ADMINS.
    Обычные пользователи могут только просматривать свои документы или одобренные администрацией
    """

    def has_permission(self, request, view):
        # Логируем безопасные методы
        print(
            f"Method: {request.method}, User: {request.user}, Is Safe Method: {request.method in permissions.SAFE_METHODS}")

        # Разрешить доступ для безопасных методов (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Логируем для POST-запросов
        if request.method == 'POST':
            print(f"POST request: User is authenticated: {request.user.is_authenticated}")
            return request.user.is_authenticated

        # Логируем, если проверяем, является ли пользователь администратором
        is_admin = self.is_admin(request.user)
        print(f"Method not safe (not GET), Admin check: {is_admin}")

        # Разрешить доступ для администраторов
        return is_admin

    def has_object_permission(self, request, view, obj):
        # Логируем данные объекта и метод
        print(
            f"Object Permission Check: Method: {request.method}, User: {request.user}, Object Status: {obj.status}, Object User: {obj.user}")

        # Разрешить доступ для безопасных методов
        if request.method in permissions.SAFE_METHODS:
            print("Safe method - access allowed")
            return True

        # Логируем для проверки администратора
        if self.is_admin(request.user):
            print("User is admin - access allowed")
            return True

        # Логируем, если это обычный пользователь, проверяем, видит ли он только свои документы или "approved"
        print(
            f"User is not admin - checking if document is approved or belongs to user: {obj.status == 'approved' or obj.user == request.user}")
        return obj.status == 'approved' or obj.user == request.user

    def is_admin(self, user):
        if user.is_staff:
            admin_emails = [email for _, email in settings.ADMINS]
            is_admin = user.email in admin_emails
            print(f"Is Admin Check: {is_admin}, User Staff Status: {user.is_staff}, User Email: {user.email}")
            return is_admin
        return False
