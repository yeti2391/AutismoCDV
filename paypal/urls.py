from django.urls import path
from . import views

template_name: 'paypal_app'

urlpatterns = [
    path('pago/', views.pago, name= 'pago'),
]
