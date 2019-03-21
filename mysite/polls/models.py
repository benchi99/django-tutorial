import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse

class Pregunta(models.Model):

    texto_pregunta = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField('Fecha de publicación')
    favorita = models.BooleanField('Favorito', default=False)
    
    def __str__(self):
        return self.texto_pregunta

    def ha_sido_publicado_recientemente(self):
        # Tutorial 2 
        # return self.fecha_publicacion >= timezone.now() - datetime.timedelta(days = 1)
        ahora = timezone.now()
        return ahora - datetime.timedelta(days=1) <= self.fecha_publicacion <= ahora

    ha_sido_publicado_recientemente.admin_order_field = 'fecha_publicacion'
    ha_sido_publicado_recientemente.boolean = True
    ha_sido_publicado_recientemente.short_description = '¿Ha sido publicado recientemente?'


class Eleccion(models.Model):

    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_eleccion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_eleccion