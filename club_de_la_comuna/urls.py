from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from core.admin import gerencia_admin_site

urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/", views.contacto, name="contacto"),
    path('negocios/', views.negocios_por_categoria, name='negocios'),  # Para mostrar todos los negocios
    path("elclub/", views.elclub, name="elclub"),
    path('negocios/<int:categoria_id>/', views.negocios_por_categoria, name='negocios_por_categoria'),  # Para filtrar por categoría
    path('gestion-informaticas2024/', admin.site.urls), # Cambiar la URL del admin para añadir capa extra de seguridad.
    path('negocios/categoria/<int:categoria_id>/', views.negocios_por_categoria, name='negocios_por_categoria'),
    path('chat/start/', views.start_conversation, name='start_conversation'),
    path('chat/send/', views.send_message, name='send_message'),
    path('como_unirse/', views.como_unirse, name='como_unirse'),
    path('accounts/', include('allauth.urls')),  # Incluye las URLs de allauth
    path('negocios_con_ofertas_activas/', views.negocios_con_ofertas_activas, name='negocios_con_ofertas_activas'),
    path("tarjeta/", views.generar_tarjeta, name="generar_tarjeta"),
    path('descargar_tarjeta/', views.descargar_tarjeta, name='descargar_tarjeta'),
    path('logout/success/', TemplateView.as_view(template_name='account/logout_success.html'), name='logout_success'),
    path('negocios_con_ofertas_activas/<int:categoria_id>/', views.negocios_con_ofertas_activas, name='negocios_con_ofertas_por_categoria'),
    path('gerencia-admin/', gerencia_admin_site.urls),
    



]

