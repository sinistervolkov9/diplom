from django.core.exceptions import ValidationError

FILE_SIZE_COEF = 1024 * 1024
FILE_SIZE_MB = 2  # указать в МБ

FILE_TYPE = ['pdf', 'doc', 'docx']


class FileSizeValidator:
    """Проверяет размер файла в MB"""

    def __init__(self, limit=FILE_SIZE_COEF * FILE_SIZE_MB):
        self.limit = limit

    def __call__(self, file):
        if file.size > self.limit:
            raise ValidationError(f"Размер файла не должен превышать {FILE_SIZE_MB} MB.")


class FileExtensionValidator:
    """Проверяет расширение файла"""

    def __init__(self, allowed_extensions=FILE_TYPE):
        self.allowed_extensions = allowed_extensions

    def __call__(self, file):
        ext = file.name.split('.')[-1].lower()

        if ext not in self.allowed_extensions:
            raise ValidationError(f'Недопустимое расширение файла.')
