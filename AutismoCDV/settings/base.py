"""

"""
import os
from unipath import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).ancestor(3)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v@%5!$^@_0)2h28h2m%wzc12e89i8&+=&e2dy%7cpc!1ti(+oe'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #third party
    'crispy_forms',
    #allauth
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.google',
    #mis apps:
    'apps.core',
    'apps.servicios',
    'apps.contacto',
    'apps.blog',
    'apps.store',
    'apps.content',
    'user',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AutismoCDV.urls'

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

WSGI_APPLICATION = 'AutismoCDV.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOGIN_URL = '/accounts/login/'
#AGREGO LOS SIGUIENTES REDIRECT LOGIN Y logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


#ALLAUTH
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

SITE_ID = 1


#Extra configs:

#extra Configuration
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS=True
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_AUTHENTICATION_METHOD='email'
#la siguiente linea obliga al usuario a verificar email
#ACCOUNT_EMAIL_VERIFICATION='mandatory'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL=LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL=LOGIN_REDIRECT_URL
SOCIALACCOUNT_QUERY_EMAIL=ACCOUNT_EMAIL_REQUIRED

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # credentials, or list them here:
        'APP': {
            'client_id': '534648312431-3va7tt656k8555fm2d0kb4npfquf485u.apps.googleusercontent.com',
            'secret': 'KuRqoeCCUmCcvsP9VznVbQ0L',
            'key': ''
        }
    }
}
