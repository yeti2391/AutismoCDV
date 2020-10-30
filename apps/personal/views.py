from django.shortcuts import render
from django.views import generic
from .models import Personal

# Create your views here.
class PersonalListView(generic.ListView):
    template_name = "personal/personal_list.html"
    queryset = Personal.objects.all()
    #paginate_by = 10

class PersonalDetailView(generic.DetailView):
    template_name="personal/personal_detail.html"
    queryset = Personal.objects.all()
