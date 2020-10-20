from django.urls import path
from .views import add_to_cart, remove_from_cart

app_name='cart_app'

urlpatterns = [
    path('add-to-cart/<course_slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<course_slug>/', remove_from_cart, name='remove-from-cart')

]
