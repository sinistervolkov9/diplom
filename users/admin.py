from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Регистрация модели User в админ-панели
    """
    list_display = ('username', 'email')
    list_filter = ('id',)
