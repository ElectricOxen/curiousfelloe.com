"""
Django settings for curiousfelloe project.
"""

from pathlib import Path
from decouple import config


APP_NAME = config('APP_NAME')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY')

DEBUG = config('DEBUG_MODE', default=False, cast=bool)

INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DOMAIN_NAME = config('DOMAIN_NAME', default='')
DEV_DOMAIN_NAME = config('DEV_DOMAIN_NAME', default='')
if DOMAIN_NAME:
    ALLOWED_HOSTS.append(DOMAIN_NAME)
if DEV_DOMAIN_NAME:
    ALLOWED_HOSTS.append(DEV_DOMAIN_NAME)

EXTRA_ALLOWED_HOSTS = config('EXTRA_ALLOWED_HOSTS', default='', cast=lambda v: [h.strip() for h in v.split(',') if h.strip()])
ALLOWED_HOSTS += EXTRA_ALLOWED_HOSTS

CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1', 'https://localhost']
if DOMAIN_NAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{DOMAIN_NAME}')
if DEV_DOMAIN_NAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{DEV_DOMAIN_NAME}')

# Azure App Service terminates TLS at the load balancer and forwards HTTP.
# This tells Django to trust the X-Forwarded-Proto header so request.scheme
# returns 'https' and generated URLs (sitemaps, canonical, OG) are correct.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_extensions',
    'rest_framework',
    'django_htmx',
    'taggit',
    'eo_site_framework',
    'landing.apps.LandingConfig',
]

TAGGIT_CASE_INSENSITIVE = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'curiousfelloe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'eo_site_framework.context_processors.brand_context',
                'eo_site_framework.context_processors.nav_context',
                'eo_site_framework.context_processors.footer_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'curiousfelloe.wsgi.application'


# Database

LOCAL_MODE = config('LOCAL_MODE', default=True, cast=bool)

if LOCAL_MODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'curiousfelloe.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DBNAME'),
            'USER': config('DBUSER'),
            'PASSWORD': config('DBPASS'),
            'HOST': config('DBHOST'),
            'PORT': config('DBPORT'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Email

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
NOTIFY_EMAIL = config('NOTIFY_EMAIL')


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

if not LOCAL_MODE:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

    WHITENOISE_MAX_AGE = 31536000


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'


# ── Curious Felloe — Site Framework Configuration ──────────────────────────
EO_FRAMEWORK = {
    'brand_name': 'Curious Felloe',
    'tagline': 'Indie Games Studio — An Electric Oxen Company',
    'copyright': '© 2026 Curious Felloe Games — An Electric Oxen LLC Company',
    'home_url_name': 'landing:home',
    'og_image_default': '/static/media/images/brand/cf-wheel.png',
    'twitter_handle': '',
    'locale': 'en_US',
    'logo': {
        'alt': 'Curious Felloe',
        'width': '48',
        'height': '48',
        'light': {
            'fallback': 'media/images/brand/cf-wheel.png',
        },
        'dark': {
            'fallback': 'media/images/brand/cf-wheel.png',
        },
    },
    'favicon': 'favicon.ico',
    'nav_links': [],
    'footer': {
        'email': 'hello@curiousfelloe.com',
        'tagline_html': (
            'Indie Games Studio.<br>'
            'An Electric Oxen Company.'
        ),
        'built_with': 'Built with Django & Tailwind CSS.',
        'social_links': [
            {'platform': 'github', 'url': 'https://github.com/ElectricOxen', 'label': 'GitHub'},
        ],
        'certifications': [],
    },
}
