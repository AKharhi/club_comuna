from django.conf import settings  # Esto ya lo tienes
from django.contrib import admin
from django.urls import path
from core import views
from django.conf.urls.static import static  # Añadir esta línea para servir archivos multimedia

urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/", views.contacto, name="contacto"),
    path("negocios/", views.lista_negocios, name="negocios"),
    path("elclub/", views.elclub, name="elclub"),
    path("admin/", admin.site.urls),
    path('crear-negocio/', views.crear_negocio, name='crear_negocio'),

]

# Solo en desarrollo, para servir archivos multimedia:


