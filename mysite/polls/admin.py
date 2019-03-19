from django.contrib import admin

from .models import Pregunta, Eleccion

class ChoiceInLine(admin.TabularInline):
    model = Eleccion
    extra = 3

class PreguntaAdmin(admin.ModelAdmin):
    # PARTE 7 REORDENAR CAMPOS EN PAGINA ADMIN
    # fields = ['fecha_publicacion', 'texto_pregunta']
    fieldsets = [
        (None,                      {'fields': ['texto_pregunta']}),
        ('Información de fecha',    {'fields': ['fecha_publicacion'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine]
    # Formato en el que se muestra la lista de preguntas
    list_display = ('texto_pregunta', 'fecha_publicacion', 'ha_sido_publicado_recientemente')
    # Campos por los que se puede filtrar la lista.
    list_filter = ['fecha_publicacion']
    # Campos por los que se puede buscar.
    search_fields = ['texto_pregunta']

admin.site.register(Pregunta, PreguntaAdmin)
# admin.site.register(Eleccion)