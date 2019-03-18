import datetime

from django.db import models
from django.utils import timezone

class Pregunta(models.Model):

    texto_pregunta = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField('Fecha de publicación')
    
    def __str__(self):
        return self.texto_pregunta
    
    def ha_sido_publicado_recientemente(self):
        return self.fecha_publicacion >= timezone.now() - datetime.timedelta(days = 1)


class Eleccion(models.Model):

    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_eleccion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_eleccion