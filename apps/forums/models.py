from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Faculty(models.Model):
    name = models.CharField(max_length=100) 
    short_name = models.CharField(max_length=15, unique=True) 
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    followers = models.ManyToManyField(User, related_name='followed_faculties', blank=True)

    def __str__(self):
        return self.short_name
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) # Ej: "Carreras", "Deportes"
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Forum(models.Model):
    title = models.CharField(max_length=100) 
    description = models.CharField(max_length=255)
    
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='forums')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='forums')
    
    def __str__(self):
        return f"[{self.category}] {self.faculty.short_name} - {self.title}"



class Thread(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='threads')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    
    # Sistema de Likes
    likes = models.ManyToManyField(User, related_name='liked_threads', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_threads', blank=True)

    def __str__(self):
        return self.title


class Reply(models.Model):
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_replies', blank=True)

    def __str__(self):
        return f"Respuesta de {self.author.username} en {self.thread.title}"
