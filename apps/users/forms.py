from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser 

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')  # campos que pedimos en el formulario de registro

# POSIBLES: form para editar perfil de usuario. form para login 