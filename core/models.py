from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import User
from datetime import date




class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    codigo_socio = models.CharField(max_length=10)
    fecha_emision = models.DateField(default=date.today)
    tarjeta_activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - Perfil de Cliente"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.nombre)
    
    def numero_negocios(self):
        return self.negocios.count() #cuenta números de negocios  # pylint: disable=no-member


#tabla oferta
class Oferta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    descripcion = models.TextField(null=True, blank=True) 
    fecha_inicio = models.DateField()  # Fecha de inicio oferta
    fecha_fin = models.DateField()  # Fecha de fin oferta
    activa = models.BooleanField(default=False)  # Indica si la oferta está activa o no

    def __str__(self):
        return str(self.nombre)


class Negocio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    # Horario de Lunes a Viernes
    apertura_lunes_viernes = models.TimeField(null=True, blank=True)
    cierre_lunes_viernes = models.TimeField(null=True, blank=True)
    # Horario de Sábados
    apertura_sabado = models.TimeField(null=True, blank=True)
    cierre_sabado = models.TimeField(null=True, blank=True)
    # Horario de Domingos y Festivos
    apertura_domingo_festivo = models.TimeField(null=True, blank=True)
    cierre_domingo_festivo = models.TimeField(null=True, blank=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, validators=[validate_email])
    descripcion = models.TextField()
    premium = models.BooleanField(default=False)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='negocios',   null=True, 
    blank=True)

    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='negocios',   null=True, 
    blank=True)  # Relación con el negocio que ofrece la promoción

    # Campo para imagen, se subirá al bucket S3 en la carpeta 'negocios/'
    imagen = models.ImageField(upload_to='negocios/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)


def __str__(self):
    return f"{self.nombre} - {self.categoria.nombre} - {self.oferta.activa}"  # pylint: disable=no-member


