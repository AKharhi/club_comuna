from django.db import models
from django.core.validators import validate_email

class Negocio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    horario = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, validators=[validate_email])
    descripcion = models.TextField()

    # Campo para imagen, se subirá al bucket S3 en la carpeta 'negocios/'
    imagen = models.ImageField(upload_to='negocios/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nombre)
