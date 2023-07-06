from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных среды из файла .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

env = environ.Env(
    DEBUG=(bool, False)
)

SECRET_KEY = env('SECRET_KEY')  # Секретный ключ проекта
DEBUG = env('DEBUG')  # Режим отладки
ALLOWED_HOSTS = ["*"]  # Разрешенные хосты для приложения

INSTALLED_APPS = [
    'django.contrib.admin',  # Административный интерфейс Django
    'django.contrib.auth',  # Аутентификация и авторизация пользователей
    'django.contrib.contenttypes',  # Модели содержимого
    'django.contrib.sessions',  # Управление сессиями
    'django.contrib.messages',  # Система сообщений
    'django.contrib.staticfiles',  # Статические файлы
    'rest_framework',  # Фреймворк для создания API
    'social_django',  # Интеграция социальной авторизации
    'django_filters',  # Фильтрация данных
    'pytest',
    'pytest_django',
    'core',  # Приложение ядра
    'goals',  # Приложение для целей
    'bot',  # Приложение для бота
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Middleware для обеспечения безопасности
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware для управления сессиями
    'django.middleware.common.CommonMiddleware',  # Общий Middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # Middleware для защиты от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Middleware для аутентификации пользователей
    'django.contrib.messages.middleware.MessageMiddleware',  # Middleware для обработки сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Middleware для защиты от кликовой атаки
]

ROOT_URLCONF = 'todolist.urls'  # Корневой URL-конфигурации
AUTH_USER_MODEL = 'core.User'  # Модель пользователя

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend шаблонов Django
        'DIRS': [BASE_DIR / 'templates'],  # Пути к директориям с шаблонами
        'APP_DIRS': True,  # Поиск шаблонов внутри приложений
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

WSGI_APPLICATION = 'todolist.wsgi.application'  # WSGI-приложение

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Драйвер базы данных PostgreSQL
        'NAME': env('DB_NAME'),  # Название базы данных
        'USER': env('DB_USER'),  # Имя пользователя базы данных
        'PASSWORD': env('DB_PASSWORD'),  # Пароль пользователя базы данных
        'HOST': env('DB_HOST', default='127.0.0.1'),  # Хост базы данных
        'PORT': '5432',  # Порт базы данных
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Валидатор схожести атрибутов пользователя
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Валидатор минимальной длины пароля
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Валидатор общих паролей
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Валидатор числовых паролей
    },
]

LANGUAGE_CODE = 'en-us'  # Язык проекта
TIME_ZONE = 'UTC'  # Часовой пояс
USE_I18N = True  # Использование международных настроек
USE_TZ = True  # Использование часового пояса

STATIC_URL = '/static/'  # URL для статических файлов
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Тип поля для автоинкрементного первичного ключа

SOCIAL_AUTH_JSONFIELD_ENABLED = True  # Использование JSONField для настроек социальной авторизации
SOCIAL_AUTH_VK_OAUTH2_KEY = env('VK_OAUTH_KEY')  # Ключ VK OAuth2
SOCIAL_AUTH_VK_OAUTH2_SECRET = env('VK_OAUTH_SECRET')  # Секретный ключ VK OAuth2
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'  # URL для перенаправления после успешной авторизации
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/logged-in/'  # URL для перенаправления после успешной регистрации нового пользователя
SOCIAL_AUTH_USER_MODEL = 'core.User'  # Модель пользователя для социальной авторизации
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']  # Разрешенные права для VK OAuth2
AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',  # Backend для авторизации через VK OAuth2
    'django.contrib.auth.backends.ModelBackend',  # Backend для авторизации через модель пользователя
)

BOT_TOKEN = env("BOT_TOKEN")  # Токен для бота
