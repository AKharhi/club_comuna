
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/", views.contacto, name="contacto"),
    path("negocios/", views.negocios, name="negocios"),
    path("elclub/", views.elclub, name="elclub"),
    path("admin/", admin.site.urls),
    
]
