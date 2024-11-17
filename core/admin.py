from django.contrib import admin
from django.utils.html import format_html
from core.models import *
from django.contrib.admin import AdminSite

class GerenciaAdmin(AdminSite): #clase personalizada que hereda de Admin para el mantenedor de la app
    site_header = "Administración del Club de la Comuna"
    site_title = "Panel de Negocios y Clientes"
    index_title = "Bienvenido al Panel de Administración del Club de la Comuna"

gerencia_admin_site = GerenciaAdmin(name='gerencia_admin') #Sólo para el mantenedor de la app.

class NegocioAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista del admin
    list_display = ('nombre', 'direccion', 'telefono', 'email', 'ver_imagen', 'created', 'updated')
    list_filter = ('created', 'updated')  # Filtros en el admin
    search_fields = ('nombre', 'direccion', 'telefono', 'email')  # Búsqueda rápida
    readonly_fields = ('created', 'updated')  # Campos de solo lectura

    # Método para mostrar la imagen en la vista del admin
    def ver_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.imagen.url)
        return "No hay imagen"
    ver_imagen.short_description = "Imagen"

# Registro del modelo Negocio con su configuración personalizada en el admin

admin.site.register(Negocio, NegocioAdmin)
admin.site.register(Categoria)
admin.site.register(Oferta)

# Registro del modelo Negocio con su configuración personalizada para el mantenedor
gerencia_admin_site.register(Negocio, NegocioAdmin)
gerencia_admin_site.register(Categoria)
gerencia_admin_site.register(Oferta)

@admin.register(ClienteProfile)
class ClienteProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'codigo_socio', 'fecha_emision', 'tarjeta_activa']
    list_filter = ['tarjeta_activa']
    search_fields = ['user__username', 'codigo_socio']