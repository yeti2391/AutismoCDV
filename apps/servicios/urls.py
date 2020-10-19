from django.urls import path
from . import views

app_name='servicios_app'

urlpatterns = [
    path('servicios/', views.servicios, name="servicios"),
]
