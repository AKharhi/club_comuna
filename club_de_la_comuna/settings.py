import os
from pathlib import Path
import dj_database_url
import environ
import logging
import boto3

<<<<<<< HEAD
# Configuración del logger para rastrear recursos de boto3
boto3.set_stream_logger('boto3.resources', logging.INFO)

# ==============================================
# BASE DIRECTORY & ENVIRONMENT VARIABLES
# ==============================================
=======
# Base directory
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializa las variables de entorno
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

<<<<<<< HEAD
# ==============================================
# SECURITY SETTINGS
# ==============================================
SECRET_KEY = env('SECRET_KEY', default='django-insecure-default-key-for-development')
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# ==============================================
# APPLICATION DEFINITION
# ==============================================
=======
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-default-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

# ALLOWED_HOSTS
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])
print("ALLOWED_HOSTS:", ALLOWED_HOSTS)

# Application definition
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
<<<<<<< HEAD
    'storages',  # Gestión de archivos con S3
    'core',      # Tu aplicación principal
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Archivos estáticos optimizados
=======
    'storages',  # Asegúrate de que 'storages' está en INSTALLED_APPS
    'core'
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "club_de_la_comuna.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "club_de_la_comuna.wsgi.application"

<<<<<<< HEAD
# ==============================================
# DATABASE CONFIGURATION
# ==============================================
DATABASE_URL = env('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
    )
}

# ==============================================
# PASSWORD VALIDATION
# ==============================================
=======
# Database configuration
DATABASE_URL = env('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
    print("Using Database URL:", DATABASE_URL)  # Para depuración
else:
    print("No DATABASE_URL found in environment variables")  # Para depuración

# Password validation
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

<<<<<<< HEAD
# ==============================================
# INTERNATIONALIZATION
# ==============================================
=======
# Internationalization
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

<<<<<<< HEAD
# ==============================================
# STATIC FILES CONFIGURATION (CSS, JavaScript)
# ==============================================
=======
# Static files (CSS, JavaScript, Images)
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

<<<<<<< HEAD
# ==============================================
# AWS S3 CONFIGURATION FOR MEDIA FILES
# ==============================================
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
=======
# Configuración para archivos multimedia (Diferente entre desarrollo y producción)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True


AWS_QUERYSTRING_EXPIRE = 600

    

    # Definir el dominio de S3
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Configurar la URL de acceso a los archivos multimedia en S3
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

    # Definir el almacenamiento de archivos multimedia en S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Parámetros adicionales para mejorar la gestión de archivos
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # Cacheo de un día
}
AWS_DEFAULT_ACL = None  # Sin permisos públicos por defecto
AWS_S3_FILE_OVERWRITE = False  # Evita sobreescribir archivos existentes
AWS_QUERYSTRING_AUTH = False  # URLs públicas sin autenticación de consulta

# ==============================================
# STORAGE CONFIGURATION
# ==============================================
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",  # Gestión de archivos multimedia
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",  # Gestión de archivos estáticos
    },
}

# ==============================================
# SECURITY SETTINGS FOR PRODUCTION
# ==============================================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ==============================================
# PRIMARY KEY FIELD TYPE
# ==============================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SSL y seguridad en producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
