from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ClienteProfile
from datetime import date
import random

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ClienteProfile.objects.create(
            user=instance,
            codigo_socio=generar_codigo_socio(),  # Genera un código de socio automáticamente
            fecha_emision=date.today(),           # Fecha de emisión es la fecha actual
            tarjeta_activa=True                   # Activa la tarjeta por defecto
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.clienteprofile.save()

# Función para generar el código de socio automáticamente
def generar_codigo_socio():
    # Aquí puedes personalizar la lógica para generar el código de socio.
    # En este caso, usamos un número aleatorio de 4 dígitos con una letra "A" al final.
    return f"cdlc-{random.randint(1000, 9999)}A"
