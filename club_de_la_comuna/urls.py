from django.contrib import admin
from django.urls import path, include
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
    path('como_unirse/', views.como_unirse, name='como_unirse'),
    path('usuario_logueado/', views.usuario_logueado, name='usuario_logueado'),
    path('accounts/', include('allauth.urls')),  # Incluye las URLs de allauth
    path('negocios_con_ofertas_activas/', views.negocios_con_ofertas_activas, name='negocios_con_ofertas_activas'),
    path("tarjeta/", views.generar_tarjeta, name="generar_tarjeta"),
    path('descargar_tarjeta/', views.descargar_tarjeta, name='descargar_tarjeta'),

]
