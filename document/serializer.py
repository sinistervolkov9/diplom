from rest_framework import serializers
from .models import Document
from .validators import FileSizeValidator, FileExtensionValidator


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'user', 'file', 'title', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'file', 'created_at']

    def validate_file(self, value):
        """
        Валидация размера и расширения загружаемого файла
        """
        FileSizeValidator()(value)         # Проверка размера файла
        FileExtensionValidator()(value)    # Проверка расширения файла
        return value

    def validate(self, attrs):
        """
        Общая валидация данных (можно добавить дополнительные проверки)
        """
        return attrs
