from django.db import models
from django.core.validators import validate_email


class Negocio(models.Model):
    nombre = models.CharField(max_length=100)  # Agregué max_length
    direccion = models.CharField(max_length=200)  # Agregué max_length
    horario = models.CharField(max_length=100)  # Agregué max_length
    telefono = models.CharField(max_length=15)  # Agregué max_length (puede variar dependiendo del formato de teléfono)
    email = models.EmailField(max_length=100, validators=[validate_email])

    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='negocios/')  # Agregué un valor para upload_to para definir el directorio
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nombre)  # Convertimos el valor a una cadena


