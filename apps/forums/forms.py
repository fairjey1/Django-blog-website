from django import forms
from .models import Reply, Thread

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = {'title', 'text'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribí tu mensaje aca...'}),}

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = {'text'}
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribí tu respuesta aca...'}),}
