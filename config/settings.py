import os
from datetime import timedelta
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Административные Email для получения уведомлений и управления документами
# Дополните, если требуется
ADMINS = [
    ('csuAdmin', 'admin@admin.ru'),
    ('Admin', os.getenv('ADMIN_EMAIL')),  # Использует email из .env
]

# Указать максимальный допустимый размер отправляемого файла в MB (для валидации)
FILE_SIZE_MB = int(os.getenv('FILE_SIZE_MB'))

# Базовая директория проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ключ безопасности для продакшена
SECRET_KEY = os.getenv('SECRET_KEY')

# Включение/отключение режима отладки
DEBUG = os.getenv('DEBUG') == 'True'

# Разрешённые хосты
ALLOWED_HOSTS = []

# Определение установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Пользовательские приложения
    'users',
    'document',

    # Сторонние приложения
    'rest_framework_simplejwt',
    'drf_yasg',
]

# Настройки промежуточного ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Конфигурация URL
ROOT_URLCONF = 'config.urls'

# Настройка шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение
WSGI_APPLICATION = 'config.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Конфигурация REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'diplom',
    'DESCRIPTION': 'Description of diplom',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Настройки JWT токенов
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Настройки интернационализации
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Пути к статическим и медиа файлам
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Стандартный тип поля для автоматического создания первичных ключей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки пользовательской модели пользователя
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'users:login'

# Конфигурация отправки email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False) == 'True'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Настройки Celery для работы с Redis
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {}

# Настройки Swagger
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

# Настройки для доверенных доменов и CSRF токенов
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
]

# Настройки безопасности сессий и CSRF
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
