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
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL= 'autismocdv@gmail.com'
EMAIL_HOST_PASSWORD = 'Marco.1234'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

#paypal AUN NO LOS LLAME EN EL CODIGO NI CONFIGURE PARA Q LEAN ESTAS LINEAS
PAYPAL_CLIENT_ID  = "AbyTJKwLUxHVds6t59uuHQ72ANO9vIDp1LnRV-2dppHPglV_SxhqyVZh09IwnBDPaYW1urYxPNfgbPbm"
PAYPAL_SECRET_ID  =  "EMEfyVXgJyorQGNCC-R8a3x2W5X69HVhbsq1rokcpCua2amqtdFEdoK_Ax7OzNGenB-xP3SEHVsM2oYU"
