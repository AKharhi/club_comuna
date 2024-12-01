from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages  # Para manejar mensajes flash
from django.contrib.auth.decorators import login_required
from core.models import Negocio, Categoria, Oferta
from .forms import ContactForm
import requests
import boto3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from itertools import zip_longest


@login_required
def generar_tarjeta(request):
    # Obtener la información del usuario y su perfil de cliente
    user = request.user
    try:
        profile = user.clienteprofile
    except AttributeError:
        return HttpResponse("No se pudo obtener el perfil del cliente", status=404)

    # Configuración del fondo y los colores
    fondo_color = (50, 50, 50)  # Gris oscuro
    texto_color = (255, 140, 0)  # Naranja

    # Crear una imagen en modo RGBA para permitir transparencia
    width, height = 450, 280
    img = Image.new("RGBA", (width, height), fondo_color)
    
    # Crear una máscara para aplicar bordes redondeados
    mask = Image.new("L", (width, height), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([(0, 0), (width, height)], radius=30, fill=255)  # Ajusta el radio de redondeo

    # Aplicar la máscara para redondear las esquinas de la imagen
    img.putalpha(mask)

    # Cargar el logotipo y redimensionarlo
    logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'images', 'logoA.PNG')
    if not os.path.exists(logo_path):
        return HttpResponse(f"Logotipo no encontrado en la ruta: {logo_path}", status=404)

    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.resize((100, 100))
    img.paste(logo, (175, 20), logo)  # Centrar el logotipo

    # Cargar una fuente para el texto
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # Dibujar la información del usuario
    draw = ImageDraw.Draw(img)
    draw.text((20, 140), f"Nombre del Cliente: {user.first_name} {user.last_name}", fill=texto_color, font=font)
    draw.text((20, 170), f"Correo Verificado: {user.email}", fill=texto_color, font=font)
    draw.text((20, 200), f"Código de Socio: {profile.codigo_socio}", fill=texto_color, font=font)
    draw.text((20, 230), f"Fecha Emisión: {profile.fecha_emision}", fill=texto_color, font=font)

    # Convertir la imagen a bytes
    buffer = BytesIO()
    img = img.convert("RGB")  # Convertir a RGB antes de guardar como PNG
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Configurar boto3 para subir a S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3_key = f"tarjetas/{user.username}_tarjeta.png"

    # Subir la imagen a S3
    s3.upload_fileobj(buffer, bucket_name, s3_key, ExtraArgs={'ContentType': 'image/png'})

    # Generar una URL prefirmada para la descarga segura
    image_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_key},
        ExpiresIn=3600  # La URL expira en 1 hora
    )

    # Pasar la URL al contexto para mostrarla en el template
    return render(request, 'core/tarjeta.html', {'image_url': image_url})



@login_required
def descargar_tarjeta(request):
    user = request.user
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3_key = f"tarjetas/{user.username}_tarjeta.png"

    # Descargar el archivo desde S3
    try:
        s3_object = s3.get_object(Bucket=bucket_name, Key=s3_key)
        file_content = s3_object['Body'].read()

        # Crear una respuesta HTTP con el contenido del archivo
        response = HttpResponse(file_content, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{user.username}_tarjeta.png"'
        return response
    except s3.exceptions.NoSuchKey:
        return HttpResponse("Tarjeta no encontrada.", status=404)
    except Exception as e:
        return HttpResponse(f"Error al descargar la tarjeta: {e}", status=500)


def home(request):
   # Filtra los primeros 6 negocios con ofertas activas para el banner
    negocios_con_ofertas_activas = list(Negocio.objects.filter(oferta__activa=True)[:6])
  # pylint: disable=no-member
    
    # Divide los negocios en grupos de tres para el banner
    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    grupos_negocios = list(grouper(negocios_con_ofertas_activas, 3))
    
    # Filtra solo los negocios que son premium
    negocios_premium = Negocio.objects.filter(premium=True)[:3]

    # Obtener todos los negocios con su dirección y nombre
    negocios = Negocio.objects.values('nombre', 'direccion')
    
    return render(request, 'core/home.html', {
        'grupos_negocios': grupos_negocios,
        'negocios_premium': negocios_premium,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })

def contacto(request):
    return render(request, "core/contacto.html")

def elclub(request):
    return render(request, "core/elclub.html")


def como_unirse(request):
    return render(request, "core/como_unirse.html")

def lista_negocios(request):
    negocios = Negocio.objects.all()  # pylint: disable=no-member  # 
    return render(request, 'core/negocios.html', {'negocios': negocios})

def negocios_por_categoria(request, categoria_id=None):
    categorias = Categoria.objects.all()  # Obtiene todas las categorías
    categoria_seleccionada = None

    if categoria_id:  # Si se proporciona un ID de categoría
        categoria_seleccionada = get_object_or_404(Categoria, id=categoria_id)
        negocios = Negocio.objects.filter(categoria=categoria_seleccionada)  # Filtra los negocios
    else:
        negocios = Negocio.objects.all()  # Muestra todos los negocios si no se selecciona una categoría

    return render(request, 'core/negocios.html', {
        'negocios': negocios,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    })




def negocios_con_ofertas_activas(request, categoria_id=None):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    categoria_seleccionada = None

    if categoria_id:  # Si se selecciona una categoría
        categoria_seleccionada = get_object_or_404(Categoria, id=categoria_id)
        negocios = Negocio.objects.filter(categoria=categoria_seleccionada, oferta__activa=True)
    else:  # Si no se selecciona categoría, mostrar todas las ofertas activas
        negocios = Negocio.objects.filter(oferta__activa=True)

    return render(request, 'core/negocios_con_ofertas_activas.html', {
        'negocios': negocios,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    })

#Vista2 Chatbot Clubcito (Ventana)
REPLIT_BOT_URL = "https://a1e941e0-0052-4d88-931b-1a97ba107373-00-2dox5ng8dzsii.kirk.replit.dev/"  # URL del bot en Replit

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



