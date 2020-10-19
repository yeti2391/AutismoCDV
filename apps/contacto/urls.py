from django.urls import path
from . import views

app_name = 'contacto_app'

urlpatterns = [
    path('contacto/', views.contact, name="contacto"),
    #path('send_mail', views.send_mail, name='plain_email')
]
