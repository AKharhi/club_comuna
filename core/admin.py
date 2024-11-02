from django.contrib import admin
from django.utils.html import format_html
from core.models import *

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