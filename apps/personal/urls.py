from django.urls import path
from .views import PersonalListView, PersonalDetailView

app_name='personal_app'

urlpatterns = [
    path("personal/", PersonalListView.as_view(), name='personal-list'),
    path("personal/<slug>/", PersonalDetailView.as_view(), name='personal-detail'),
    #probar sacar slug y usar como pk: id

]
