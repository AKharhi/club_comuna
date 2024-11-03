# core/forms.py
from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre", required=True, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan', 'class': 'form-control'}))
    apellido = forms.CharField(max_length=100, label="Apellido", required=True, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Pérez', 'class': 'form-control'}))
    celular = forms.CharField(max_length=20, label="Celular", required=True, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: +56 9 1234 5678', 'class': 'form-control'}))
    email = forms.EmailField(label="Correo Electrónico", required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ejemplo: correo@ejemplo.com', 'class': 'form-control'}))
    comentario = forms.CharField(label="Comentario", required=True, widget=forms.Textarea(attrs={'placeholder': 'Escribe tu comentario aquí...', 'class': 'form-control', 'rows': 4}))
