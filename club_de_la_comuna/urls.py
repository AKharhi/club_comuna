from django.conf import settings  # Esto ya lo tienes
from django.contrib import admin
from django.urls import path
from core import views
from django.conf.urls.static import static  # Añadir esta línea para servir archivos multimedia
from core.views import *

urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/", views.contacto, name="contacto"),
    path("negocios/", views.lista_negocios, name="negocios"),
    path("elclub/", views.elclub, name="elclub"),
    path("admin/", admin.site.urls),
    path('negocios/', negocios_por_categoria, name='negocios'),
    path('negocios/categoria/<int:categoria_id>/', negocios_por_categoria, name='negocios_por_categoria'),
    path('chat/start/', views.start_conversation, name='start_conversation'),
    path('chat/send/', views.send_message, name='send_message'),
]
