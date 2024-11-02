from django.shortcuts import render, get_object_or_404, redirect
from core.models import *
from django.conf import settings
from django.shortcuts import render
import requests
from django.http import JsonResponse

# def home(request):
#     return render(request, 'core/home.html', {
#         'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
#     })




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

def negocios_por_categoria(request):
    categoria_id = request.GET.get('categoria')
    categorias = Categoria.objects.all()  # Todas las categorías # pylint: disable=no-member

    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id)
        negocios = Negocio.objects.filter(categoria=categoria)  # Negocios filtrados por categoría # pylint: disable=no-member
    else:
        negocios = Negocio.objects.all()  # Todos los negocios # pylint: disable=no-member

    return render(request, 'core/negocios.html', {
        'negocios': negocios,
        'categorias': categorias,
        'categoria_seleccionada': int(categoria_id) if categoria_id else None,
    })

#Vista2 Chatbot Clubcito (Ventana)
REPLIT_BOT_URL = "https://a1e941e0-0052-4d88-931b-1a97ba107373-00-2dox5ng8dzsii.kirk.replit.dev//"  # URL del bot en Replit

def start_conversation(request):
    response = requests.get(f"{REPLIT_BOT_URL}/start")
    return JsonResponse(response.json())

def send_message(request):
    message = request.POST.get('message')
    thread_id = request.POST.get('thread_id')

    payload = {
        'message': message,
        'thread_id': thread_id,
    }
    response = requests.post(f"{REPLIT_BOT_URL}/chat", json=payload)
    return JsonResponse(response.json())

