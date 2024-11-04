from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from core.models import Negocio, Categoria
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.contrib import messages  # Para manejar mensajes flash
from core.models import Negocio, Oferta
import requests
from itertools import zip_longest

REPLIT_BOT_URL = "https://a1e941e0-0052-4d88-931b-1a97ba107373-00-2dox5ng8dzsii.kirk.replit.dev/"  # URL del bot en Replit

def home(request):
   # Filtra los negocios que tienen ofertas activas
    negocios_con_ofertas_activas = Negocio.objects.filter(oferta__activa=True)  # pylint: disable=no-member
    
    # Divide los negocios en grupos de tres para el banner
    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    grupos_negocios = list(grouper(negocios_con_ofertas_activas, 3))
    
    # Filtra solo los negocios que son premium
    negocios_premium = Negocio.objects.filter(premium=True)[:3]
    
    return render(request, 'core/home.html', {
        'grupos_negocios': grupos_negocios,
        'negocios_premium': negocios_premium,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })

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

def negocios_con_ofertas_activas(request):
    # Filtra solo las ofertas activas
    ofertas_activas = Oferta.objects.filter(activa=True)  # pylint: disable=no-member
    # Filtra los negocios que están asociados a ofertas activas
    negocios = Negocio.objects.filter(oferta__in=ofertas_activas)  # pylint: disable=no-member

    return render(request, 'core/negocios_con_ofertas.html', {
        'negocios': negocios,
        'ofertas_activas': ofertas_activas,
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


def contacto(request):
    form_submitted = False  # Variable para controlar la visibilidad del formulario

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            celular = form.cleaned_data['celular']
            email = form.cleaned_data['email']
            comentario = form.cleaned_data['comentario']
            
            # Enviar el correo
            send_mail(
                subject=f"Contacto de {nombre} {apellido}",
                message=f"Nombre: {nombre} {apellido}\nCelular: {celular}\nCorreo: {email}\nComentario:\n{comentario}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Cambia este correo por el que deseas recibir el mensaje
            )
            
            # Envía un mensaje de éxito y oculta el formulario
            messages.success(request, 'Gracias por su mensaje. Nos pondremos en contacto pronto.')
            form_submitted = True  # Cambia a True para ocultar el formulario
    else:
        form = ContactForm()

    return render(request, 'core/contacto.html', {'form': form, 'form_submitted': form_submitted})