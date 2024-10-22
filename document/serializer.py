from rest_framework import serializers
from .models import Document
from .validators import FileSizeValidator, FileExtensionValidator


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'created_at', 'updated_at']

    def validate(self, value):
        # Проверяет размер файла в MB
        FileSizeValidator()(value)

        # Проверяет расширение файла
        FileExtensionValidator()(value)

        return value
