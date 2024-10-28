from rest_framework import serializers
from .models import Document
from .validators import FileSizeValidator, FileExtensionValidator


class DocumentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Document, содержащий поля для создания, просмотра и валидации документа.
    - `file`: Файл, который необходимо загрузить (поддерживаемые форматы и размер проверяются).
    - `title`: Название документа.
    - `status`: Статус документа (устанавливается по умолчанию как 'pending' и не редактируется пользователем).
    - `user`: Автор документа, автоматически присваивается текущий пользователь.
    """
    class Meta:
        model = Document
        fields = ['id', 'user', 'file', 'title', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate_file(self, value):
        """
         Проверяет файл на соответствие установленным ограничениям:
         - Размер файла
         - Формат файла
         """
        FileSizeValidator()(value)       # Проверка размера файла
        FileExtensionValidator()(value)  # Проверка расширения файла
        return value

    def validate(self, attrs):
        """
        Общая валидация данных (можно добавить дополнительные проверки)
        """
        return attrs

    def create(self, validated_data):
        """
        При создании нового документа устанавливает статус 'pending'
        """
        validated_data['status'] = 'pending'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Обновляет документ, при этом запрещая изменение поля 'file' при PUT- и PATCH-запросах.
        """
        validated_data.pop('file', None)
        return super().update(instance, validated_data)
