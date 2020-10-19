from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
#en produccion cambiar STATICFILES_DIRS a STATIC_ROOT y ejecutrar el comando
# python manage.py collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')



# Email config cambiar a google para probar
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL= 'ongautismouy@gmail.com'
EMAIL_HOST_PASSWORD = 'Salus4349324'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
