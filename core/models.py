from django.db import models
from django.core.validators import validate_email



class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.nombre)
    
    def numero_negocios(self):
        return self.negocios.count() #cuenta números de negocios  # pylint: disable=no-member

    
class Negocio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    horario = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, validators=[validate_email])
    descripcion = models.TextField()

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='negocios',   null=True, 
    blank=True)

    # Campo para imagen, se subirá al bucket S3 en la carpeta 'negocios/'
    imagen = models.ImageField(upload_to='negocios/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

def __str__(self):
    return f"{self.nombre} - {self.categoria.nombre}"  # pylint: disable=no-member

