import os
from datetime import timedelta

# CONFIG_DIR points to config package (project/src/apps/config)
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BASE_DIR points to starting point of the projects's base directory path (<project_name>/(config, apps))
BASE_DIR = os.path.abspath(os.path.join(CONFIG_DIR, '..'))

# ASSETS_MEDIA_DIR points to the top level directory (one directory up from BASE_DIR)
# assets, media, database, and venv will be located in this directory
ASSETS_MEDIA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

# APPS_DIR points to the core package (project/src/apps).
# All custom apps and newly created apps will be located in this directory.
APPS_DIR = os.path.join(BASE_DIR, 'apps')

BUILT_IN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'debug_toolbar',
    'pymongo',
    'corsheaders',
    'rest_framework_simplejwt'
]
USER_DEFINED_APPS = [
    'apps.authentication',
    'apps.documentation',
    'apps.namegen',
    'apps.forms',
    'apps.services'
]
INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTY_APPS + USER_DEFINED_APPS


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),  #
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_ON_LOGIN': True,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': "LNAI-SECRET-KEY",
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


BUILT_IN_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
THIRD_PARTY_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware']
USER_DEFINED_MIDDLEWARE = []
MIDDLEWARE = BUILT_IN_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + USER_DEFINED_MIDDLEWARE

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangonew.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangonew.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files')  # project/core/static_files
]
STATIC_ROOT = os.path.join(ASSETS_MEDIA_DIR, 'assets')  # project/assets

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ASSETS_MEDIA_DIR, 'media')  # project/media

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:5173',
#   'http://localhost:3000',
#   'http://localhost:3001'
# )

LNAI_SECRET_TOKEN_KEY = "lnai-secret-key"
TOTAL_WORKER_THREAD = 16
MCA_LOGIN_PASS_HASH="data=Ut8pBOc0RSM6iYqffqN1ovf7bobPRWJxrpoJRNCmK3GGtEoRKl3FZEf8xy36Iw3GHkoeOLH2Iw8tFFM6yB%2F6gZ4FgTyvicwoT%2FfDKJjUEuk9iiwbfqGT4bPey9LVPXwmJrnHl2AVXwPwjTY7BjtpUZ7CCRrYzb8G8Hs%2FTqLxp0oBRcfBtzGPnIVN9fMdkw%2Fj%2FSvMTL%2FNk05TbSN%2FPlQW%2FgdaTJRMuzmlIKp26ixHs8k%3D"
