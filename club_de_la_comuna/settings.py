import os
from pathlib import Path
import dj_database_url
import environ
import logging
import boto3

# Configuración del logger para rastrear recursos de boto3
boto3.set_stream_logger('boto3.resources', logging.INFO)

# ==============================================
# BASE DIRECTORY & ENVIRONMENT VARIABLES
# ==============================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializa las variables de entorno
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ==============================================
# SECURITY SETTINGS
# ==============================================
SECRET_KEY = env('SECRET_KEY', default='django-insecure-default-key-for-development')
DEBUG = True  # Cambiar a False en producción
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# ==============================================
# APPLICATION DEFINITION
# ==============================================
INSTALLED_APPS = [
    'django.contrib.sites',  # Necesario para django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'storages',  # Gestión de archivos con S3
    'core',  # Aplicación principal
    "corsheaders",  # Para manejo de CORS, útil para APIs
    'django_extensions',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Opcional para archivos estáticos
    "corsheaders.middleware.CorsMiddleware",  # Opcional para CORS
    "allauth.account.middleware.AccountMiddleware",  # Middleware de allauth
]
# ==============================================
# CORS CONFIGURATION
# ==============================================
CORS_ALLOWED_ORIGINS = [
    "https://3280a653-bce3-4755-b076-9d26aea1d67b-00-1yju02xjv8g7k.spock.replit.dev",
    "https://accounts.google.com"
]

# ==============================================
# URL CONFIGURATION
# ==============================================
ROOT_URLCONF = "club_de_la_comuna.urls"
WSGI_APPLICATION = "club_de_la_comuna.wsgi.application"

# ==============================================
# TEMPLATES CONFIGURATION
# ==============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],  # Debe incluir la carpeta 'templates'
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
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================
# INTERNATIONALIZATION
# ==============================================
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==============================================
# STATIC FILES CONFIGURATION (CSS, JavaScript)
# ==============================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================
# AWS S3 CONFIGURATION FOR MEDIA FILES
# ==============================================
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

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

# ==============================================
# GOOGLE MAPS API KEY
# ==============================================
GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY', default='')

# ==============================================
# AUTHENTICATION BACKENDS
# ==============================================
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ==============================================
# SESSION CONFIGURATION
# ==============================================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ==============================================
# django-allauth CONFIGURATION
# ==============================================
SITE_ID = 3
LOGIN_REDIRECT_URL = '/'  # Redirige al inicio o donde prefieras
LOGOUT_REDIRECT_URL = '/logout/success/'  # Redirige a una página personalizada
  # Ajusta este valor al path correspondiente a tu template

# Configuración de django-allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'CLIENT_ID': '200853372326-g42lob8cskpnuu30e4cdbo4phgcu9jl5',
        'SECRET': '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',
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True

# ==============================================
# LOGGING CONFIGURATION
# ==============================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# ==============================================
# EMAIL CONFIGURATION
# ==============================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'informaticas.aconcagua@gmail.com'
EMAIL_HOST_PASSWORD = 'jrctnthnqzwtpglv' #contraseña de aplicación de cuenta gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
