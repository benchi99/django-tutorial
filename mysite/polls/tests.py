import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Pregunta

def crear_pregunta(texto_pregunta_nueva, dias):
        """
        Crea una pregunta con el `texto_pregunta` dado y publicada
        un numero de días en el futuro en función a el momento en el que se
        ejecute la funcion. (Valores negativos para preguntas en el pasado, 
        valores positivos para preguntas en el futuro.)
        """
        hora = timezone.now() + datetime.timedelta(days=dias)
        return Pregunta.objects.create(texto_pregunta = texto_pregunta_nueva, fecha_publicacion = hora)


class PreguntaModeloTest(TestCase):
    
    def test_ha_sido_publicado_recientemente_con_pregunta_futura(self):
        """
        ha_sido_publicado_recientemente() debe devolver Falso para
        aquellas preguntas que tengan fecha_publicación en el futuro.
        """
        hora = timezone.now() + datetime.timedelta(days=30)
        pregunta_futura = Pregunta(fecha_publicacion = hora)
        self.assertIs(pregunta_futura.ha_sido_publicado_recientemente(), False)

    def test_ha_sido_publicado_recientemente_con_pregunta_antigua(self):
        hora = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pregunta_antigua = Pregunta(fecha_publicacion = hora)
        self.assertIs(pregunta_antigua.ha_sido_publicado_recientemente(), False)

    def test_ha_sido_publicado_recientemente_con_pregunta_reciente(self):
        hora = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pregunta_reciente = Pregunta(fecha_publicacion = hora)
        self.assertIs(pregunta_reciente.ha_sido_publicado_recientemente(), True)

    
class PreguntaIndexViewTests(TestCase):
    
    def test_no_hay_preguntas(self):
        """
        En caso de que no haya preguntas, que muestre el mensaje apropiado.
        """
        respuesta = self.client.get(reverse('polls:index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "No hay preguntas disponibles.")
        self.assertQuerysetEqual(respuesta.context['lista_preguntas_recientes'], [])

    def test_preguntas_antiguas(self):
        """
        Aquellas preguntas que su fecha_publicación estén en el pasado
        deben ser mostradas
        """
        crear_pregunta(texto_pregunta_nueva="Pregunta antigua", dias=-30)
        respuesta = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            respuesta.context['lista_preguntas_recientes'],
            ['<Pregunta: Pregunta antigua>']
        )

    def test_pregunta_futura(self):
        """
        Aquellas preguntas que su fecha_publicación estén en el futuro, no deben mostrarse.
        """
        crear_pregunta(texto_pregunta_nueva="Pregunta futura", dias=30)
        respuesta = self.client.get(reverse('polls:index'))
        self.assertContains(respuesta, "No hay preguntas disponibles.")
        self.assertQuerysetEqual(respuesta.context['lista_preguntas_recientes'], [])
    
    def test_pregunta_futura_y_pasada(self):
        """
        Aunque haya preguntas pasadas y futuras, deberán solo mostrarse preguntas en el pasado.
        """
        crear_pregunta(texto_pregunta_nueva="Pregunta futura", dias=30)
        crear_pregunta(texto_pregunta_nueva="Pregunta antigua", dias=-30)
        respuesta = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            respuesta.context['lista_preguntas_recientes'],
            ['<Pregunta: Pregunta antigua>']
        )

    def test_dos_preguntas_antiguas(self):
        """
        El índice deberá mostrar múltiples preguntas.
        """
        crear_pregunta(texto_pregunta_nueva="Pregunta antigua 1", dias=-30)
        crear_pregunta(texto_pregunta_nueva="Pregunta antigua 2", dias=-5)
        respuesta = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            respuesta.context['lista_preguntas_recientes'],
            ['<Pregunta: Pregunta antigua 2>', '<Pregunta: Pregunta antigua 1>']
        )

class PreguntaDetalleViewTests(TestCase):
    
    def test_pregunta_futura(self):
        """
        El detalle de una pregunta con fecha_publicacion en el futuro debe devolver un 404.
        """

        pregunta_futura = crear_pregunta(texto_pregunta_nueva="Pregunta futura", dias=5)
        url = reverse('polls:Detalle', args=(pregunta_futura.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pregunta_pasada(self):
        """
        El detalle de una pregunta con una fecha_publicacion en el pasado debe mostrar la pregunta.
        """
        pregunta_pasada = crear_pregunta(texto_pregunta_nueva="Pregunta pasada", dias=-5)
        url = reverse('polls:Detalle', args=(pregunta_pasada.id,))
        response = self.client.get(url)
        self.assertContains(response, pregunta_pasada.texto_pregunta)
        