from django.shortcuts import render, get_object_or_404, redirect
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


def crear_negocio(request):
    if request.method == 'POST':
        try:
            imagen = request.FILES.get('imagen')

            if not imagen:
                print("⚠️ No se ha recibido ninguna imagen.")
                return redirect('home')

            negocio = Negocio.objects.create( # pylint: disable=no-member 
                nombre=request.POST['nombre'],
                direccion=request.POST['direccion'],
                horario=request.POST['horario'],
                telefono=request.POST['telefono'],
                email=request.POST['email'],
                descripcion=request.POST['descripcion'],
                imagen=imagen
            )

            print(f"✅ Imagen subida a: {negocio.imagen.url}")

        except Exception as e:
            print(f"⚠️ Error al subir la imagen: {str(e)}")

        return redirect('home')

    return render(request, 'core/home.html')