from urllib import request

from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

from django.views.generic import DetailView
from .models import CustomUser as User

# login
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('inicio')  # Redirige a la página de inicio 

# register
class CustomSignupView(CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('inicio')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: # si ya esta logueado lo redirigimos a la pagina de inicio
            return redirect('inicio')
        return super().get(request, *args, **kwargs) # si no esta logueado mostramos el formulario de registro
    
    def form_valid(self, form):
        
        response = super().form_valid(form)
        login(self.request, self.object) # Inicia sesión automáticamente después del registro
        return response

#logout
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('inicio')  # Redirige a la página de inicio después de cerrar sesión

class ProfileView(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user_profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
