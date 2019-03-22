import io
from django.http import HttpResponseRedirect, HttpResponse # , Http404
from django.utils import timezone
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .reports import generaInformeResultado
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from .models import Pregunta, Eleccion

""" TUTORIAL 3
def index(request):
    # Tutorial 2
    # return HttpResponse("Hola mundo. Este es el índice de la aplicación Polls.")
    lista_preguntas_recientes = Pregunta.objects.order_by('-fecha_publicacion')[:5]
    #cargar template creado
    template = loader.get_template('polls/index.html')
    contexto = {
        'lista_preguntas_recientes': lista_preguntas_recientes
    }
    return HttpResponse(template.render(contexto, request))
    # Ó, también se puede hacer lo siguiente:
    # return render(request, 'polls/index.html', contexto)

def detalle(request, id_pregunta):
    # Tutorial 2
    # return HttpResponse("Estás mirando la pregunta %s." % id_pregunta)
    try:
        q = Pregunta.objects.get(pk=id_pregunta)
    except Pregunta.DoesNotExist:
        raise Http404("La pregunta no existe.")
    return render(request, 'polls/detalle.html', {'pregunta': q})
    # Ó, también se puede hacer lo siguiente:
    # q = get_object_or_404(Pregunta, pk=id_pregunta)
    # return render(request, 'polls/detalle.html', {'pregunta': q})

def resultados(request, id_pregunta):
    # Tutorial 2
    # response = "Estás mirando los resultados de la pregunta %s."
    # return HttpResponse(response % id_pregunta)
    q = get_object_or_404(Pregunta, pk=id_pregunta)
    return render(request, 'polls/resultado.html', {'pregunta': q})
"""

# Vista índice.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lista_preguntas_recientes'

    def get_queryset(self):
        # Devuelve las últimas cinco preguntas
        # Tutorial 4
        # return Pregunta.objects.order_by('-fecha_publicacion') [:5]
        # Devuelve las últimas cinco preguntas (sin incluir las que están en el futuro.)
        return Pregunta.objects.filter(fecha_publicacion__lte = timezone.now()).order_by('-fecha_publicacion')[:5]

# Vista de detalle.
class DetalleView(generic.DetailView):
    model = Pregunta
    template_name = 'polls/detalle.html'

    def dispatch(self, request, *args, **kwargs):
        fav = request.GET.get('fav', '').lower()
        if fav == 'true':
            actualizarFav(True, **kwargs)
        elif fav == 'false':
            actualizarFav(False, **kwargs)
        return super(DetalleView, self).dispatch(request, *args, **kwargs)

    # Y si...
    def get_queryset(self):
        # Devuelve pregunta si está realizada en el pasado.
        return Pregunta.objects.filter(fecha_publicacion__lte = timezone.now()).order_by('-fecha_publicacion')

#Vista del resultado.
class ResultadosView(generic.DetailView):
    model = Pregunta
    template_name = 'polls/resultado.html'

# Actualiza el campo favorito de la pregunta.
def actualizarFav(valor, **kwargs):
    """"
    No get_object_or_404 ya que en un principio se ha
    accedido ya de por si al detalle de una pregunta de antemano.
    """
    q = Pregunta.objects.get(pk = kwargs['pk'])
    q.favorita = valor
    q.save()

# Vista que realiza el voto.
def voto(request, id_pregunta):
    # Tutorial 2
    # return HttpResponse("Estás votando la pregunta %s." % id_pregunta)
    q = get_object_or_404(Pregunta, pk=id_pregunta)
    try:
        eleccion_usuario = q.eleccion_set.get(pk=request.POST['eleccion'])
    except(KeyError, Eleccion.DoesNotExist):
        # Muestra de nuevo el formulario.
        return render(request, 'polls/detalle.html', {
            'pregunta': q,
            'error_message': "No has escogido nada."
        })
    else:
        eleccion_usuario.votos += 1
        eleccion_usuario.save()
        return HttpResponseRedirect(reverse('polls:Resultados', args=(q.id,)))


def exportarVotos(request, id_pregunta):
    """
    Vista que va a exportar los datos actuales de la 
    votación a un informe PDF.
    """
    # Obtengo el objeto Pregunta del cual obtenemos la información.
    q = get_object_or_404(Pregunta, pk = id_pregunta)
    
    # Se crea un objeto HttpResponse con los encabezados PDF.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_resultado-pregunta'+str(q.pk)+'.pdf"'

    # Se construye el objeto PDF, utilizando el objeto respuesta como archivo.
    # Librería de generación de PDFs: ReportLab.
    pdf = generaInformeResultado(q, response)
    
    return response
