import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '^r%264v886@33$@pz^n7j-1ne!n8&=8lcjbd_9$c(_o30awob7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'obsequiemos',
    'widget_tweaks',
    'social.apps.django_app.default',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'obsequiemos_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_TWITTER_KEY = 'i8kxaK09w8f3OZH5VOPqODWvZ'
SOCIAL_AUTH_TWITTER_SECRET = 'YPbbkExzSBQXcs0fj9eDF0FRnvh7ngZ2b2ELLC8LpnnfHNp3Pm'

SOCIAL_AUTH_FACEBOOK_KEY = '2037530789806710'
SOCIAL_AUTH_FACEBOOK_SECRET = 'a675362d40912310098dba9d7e3bfc9d'

SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/registra_social/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'obsequiemos_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'giving',
        'USER': 'alonso',
        'PASSWORD': 'alonso',
        'HOST': 'localhost',  # giving.cl#localhost
        # 'HOST': 'localhost',#localhost
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_PATH = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 1209600
