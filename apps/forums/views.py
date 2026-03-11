from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ReplyForm, ThreadForm
from .models import Faculty, Forum, Reply, Thread
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
    
class ThreadDetailView(FormMixin, DetailView):
    model = Thread
    template_name = 'forums/thread_detail.html'
    context_object_name = 'thread'
    slug_field = 'slug' 
    slug_url_kwarg = 'slug' 
    form_class = ReplyForm
    
    def get_success_url(self):
        return reverse_lazy('forums:thread_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs): # logica 
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Debes iniciar sesión para responder.")
            
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form): # donde se guarda la respuesta, asociándola al Thread y al usuario que la creó.
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.thread = self.object

        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            reply.parent_id = parent_id

        reply.save()
        return super().form_valid(form)
     
    def get_context_data(self, **kwargs): # esto es para optimizar la consulta para traer todas las respuestas con un solo query, luego armar una estructura virtual y pasarlo al front     
        context = super().get_context_data(**kwargs)
        
        all_replies = self.object.replies.select_related('author').all()
        
        # 2. Creamos un diccionario para buscar repuestas por su ID rápidamente en memoria
        reply_map = {reply.id: reply for reply in all_replies}
        
        # 3. Inicializamos una lista vacía de "hijos virtuales" en cada objeto
        for reply in all_replies:
            reply.virtual_children = []
            
        root_replies = []
        
        # 4.
        for reply in all_replies:
            if reply.parent_id is None:
                root_replies.append(reply)
            else:
                parent = reply_map.get(reply.parent_id)
                if parent:
                    parent.virtual_children.append(reply)
                    
        context['root_replies'] = root_replies
        return context

class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reply
    template_name = 'forums/reply_confirm_delete.html'

    def test_func(self):
        # Esta función de Django comprueba si el usuario tiene permiso.
        # Obtenemos el comentario que se intenta borrar.
        reply = self.get_object()
        # Devuelve True solo si el usuario logueado es el autor original.
        return self.request.user == reply.author

    def get_success_url(self):
        # Tras borrar, redirigimos de vuelta al Hilo original.
        # self.object aún guarda los datos en memoria en este punto del ciclo de vida.
        return reverse_lazy('forums:thread_detail', kwargs={'slug': self.object.thread.slug})
    
class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    template_name = 'forums/thread_confirm_delete.html'

    def test_func(self):
        thread = self.get_object()
        return self.request.user == thread.author

    def get_success_url(self):
        return reverse_lazy('forums:forum_detail', kwargs={
            'short_name': self.object.forum.faculty.short_name, 
            'slug': self.object.forum.slug
        })


