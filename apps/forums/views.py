from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import ThreadForm
from .models import Faculty, Forum
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

class ForumDetailView(FormMixin, DetailView): # formMixin para manejar el formulario de creación de Threads dentro del DetailView del Forum
    model = Forum
    template_name = 'forums/forum_detail.html'
    context_object_name = 'forum'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = ThreadForm

    def post(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Debes iniciar sesión para publicar.")
        
        self.object = self.get_object()  # FormMixin necesita acceso al objeto de la view (el Foro) para generar la URL de éxito y para que nosotros podamos asociarlo al Thread.
        
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.author = self.request.user
        thread.forum = self.object

        thread.save()
        
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        faculty_short_name = self.kwargs.get('short_name')
        forum_slug = self.kwargs.get('slug')
        
        return get_object_or_404(
            Forum, 
            slug=forum_slug, 
            faculty__short_name=faculty_short_name 
        )

    def get_success_url(self):
        return reverse_lazy('forums:forum_detail', kwargs={
            'short_name': self.object.faculty.short_name, 
            'slug': self.object.slug
        })

