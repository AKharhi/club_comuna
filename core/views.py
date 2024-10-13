from django.shortcuts import render, get_object_or_404
from core.models import *



# Create your views here.

def home(request):
    return render(request, "core/home.html")

def contacto(request):
    return render(request, "core/contacto.html")


def elclub(request):
    return render(request, "core/elclub.html")


def negocios(request):
    return render(request, "core/negocios.html")


def lista_negocios(request):
    # Obtener todos los objetos del modelo Negocio
    negocios = Negocio.objects.all()  # pylint: disable=no-member  # deshabilita la verificación en esa línea

    # Pasar los negocios al template
    return render(request, 'core/negocios.html', {'negocios': negocios})
