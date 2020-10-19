from django.urls import path
from . import views
#para ver las imagenes URL:
#from django.conf.urls.static import static
#from django.conf import settings
#agregados esos imports en url settings

app_name = 'store_app'

urlpatterns = [
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]
