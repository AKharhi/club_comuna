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
<<<<<<< HEAD
    path('crear-negocio/', views.crear_negocio, name='crear_negocio'),

]

# Solo en desarrollo, para servir archivos multimedia:

=======
]

# Solo en desarrollo, para servir archivos multimedia:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> c6ac06384790f39cd8859a53af52ad612bfa2b30

