from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) # agregamos el campo de email y lo hacemos único
    biografy = models.TextField(blank=True, null=True) # agregamos el campo de biografía, permitiendo que sea opcional
    
    def __str__(self):
        return self.username
