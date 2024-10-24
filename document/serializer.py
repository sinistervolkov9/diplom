from rest_framework import serializers
from .models import Document
from .validators import FileSizeValidator, FileExtensionValidator


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'user', 'file', 'title', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'file', 'created_at']

    def validate_file(self, value):
        # Проверяет размер файла в MB
        FileSizeValidator()(value)

        # Проверяет расширение файла
        FileExtensionValidator()(value)

        return value

    def validate(self, attrs):
        return attrs
