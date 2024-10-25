from django.core.exceptions import ValidationError
from config.settings import FILE_SIZE_MB

# Константы для ограничения размера файла и допустимых типов
FILE_SIZE_LIMIT = 1024 * 1024 * FILE_SIZE_MB  # размер файла в байтах
ALLOWED_FILE_EXTENSIONS = ['pdf', 'doc', 'docx']


class FileSizeValidator:
    """
    Валидатор для проверки размера файла (не более FILE_SIZE_MB MB)
    """

    def __init__(self, limit=FILE_SIZE_LIMIT):
        self.limit = limit

    def __call__(self, file):
        if file.size > self.limit:
            raise ValidationError(f"Размер файла не должен превышать {FILE_SIZE_MB} MB.")


class FileExtensionValidator:
    """
    Валидатор для проверки допустимого расширения файла
    """

    def __init__(self, allowed_extensions=ALLOWED_FILE_EXTENSIONS):
        self.allowed_extensions = allowed_extensions

    def __call__(self, file):
        ext = file.name.split('.')[-1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(
                f'Недопустимое расширение файла: {ext}. Допустимые расширения: {", ".join(self.allowed_extensions)}.'
            )
