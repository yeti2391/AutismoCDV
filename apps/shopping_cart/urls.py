from django.urls import path
from .views import add_to_cart, remove_from_cart, order_view

app_name='cart_app'

urlpatterns = [
    path('order-summary/', order_view, name='order-summary'),
    path('add-to-cart/<course_slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<course_slug>/', remove_from_cart, name='remove-from-cart'),


]
