from django.conf import settings  # Configuración de Django
from django.conf.urls.static import static  # Archivos estáticos y multimedia
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/", views.contacto, name="contacto"),
    path("negocios/", views.lista_negocios, name="negocios"),
    path("elclub/", views.elclub, name="elclub"),
    path("admin/", admin.site.urls),
    path('negocios/categoria/<int:categoria_id>/', views.negocios_por_categoria, name='negocios_por_categoria'),
    path('chat/start/', views.start_conversation, name='start_conversation'),
    path('chat/send/', views.send_message, name='send_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
