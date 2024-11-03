from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from core.models import Negocio, Categoria
from django.conf import settings
import requests

REPLIT_BOT_URL = "https://a1e941e0-0052-4d88-931b-1a97ba107373-00-2dox5ng8dzsii.kirk.replit.dev/"  # URL del bot en Replit

def home(request):
    negocios = Negocio.objects.all()[:3]  #  # pylint: disable=no-member  # 
    return render(request, 'core/home.html', {'negocios': negocios, 'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})

def contacto(request):
    return render(request, "core/contacto.html")

def elclub(request):
    return render(request, "core/elclub.html")


def negocios(request):
    return render(request, "core/negocios.html")

#def inicio_sesion(request):
 #   return render(request, "account/login.html")  allauth maneja la lógica

def como_unirse(request):
    return render(request, "core/como_unirse.html")

def usuario_logueado(request):
    return render(request, "core/usuario_logueado.html")

def lista_negocios(request):
    negocios = Negocio.objects.all()  # pylint: disable=no-member  # 
    return render(request, 'core/negocios.html', {'negocios': negocios})

def negocios_por_categoria(request, categoria_id):
    categorias = Categoria.objects.all()   # pylint: disable=no-member  # 
    categoria_seleccionada = get_object_or_404(Categoria, id=categoria_id)
    negocios = Negocio.objects.filter(categoria=categoria_seleccionada)  # pylint: disable=no-member  # 
    return render(request, 'core/negocios.html', {
        'negocios': negocios,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    })

def start_conversation(request):
    response = requests.get(f"{REPLIT_BOT_URL}/start")
    return JsonResponse(response.json())

def send_message(request):
    message = request.POST.get('message')
    thread_id = request.POST.get('thread_id')
    payload = {'message': message, 'thread_id': thread_id}
    response = requests.post(f"{REPLIT_BOT_URL}/chat", json=payload)
    return JsonResponse(response.json())
