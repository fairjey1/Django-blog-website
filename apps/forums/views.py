from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Faculty
# Create your views here.

class FacultyListView(ListView):
    model = Faculty
    template_name = 'forums/faculty_list.html'
    context_object_name = 'faculties'

class FacultyFeedView(DetailView):
    model = Faculty
    template_name = 'forums/faculty_feed.html'
    context_object_name = 'faculty'
    slug_field = 'short_name'
    slug_url_kwarg = 'short_name'

