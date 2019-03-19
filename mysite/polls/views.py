from django.http import HttpResponseRedirect # , HttpResponse, Http404
from django.utils import timezone
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

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

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lista_preguntas_recientes'

    def get_queryset(self):
        # Devuelve las últimas cinco preguntas
        # Tutorial 4
        # return Pregunta.objects.order_by('-fecha_publicacion') [:5]
        # Devuelve las últimas cinco preguntas (sin incluir las que están en el futuro.)
        return Pregunta.objects.filter(fecha_publicacion__lte = timezone.now()).order_by('-fecha_publicacion')[:5]


class DetalleView(generic.DetailView):
    model = Pregunta
    template_name = 'polls/detalle.html'

    # Y si...
    def get_queryset(self):
        # Devuelve pregunta si está realizada en el pasado.
        return Pregunta.objects.filter(fecha_publicacion__lte = timezone.now()).order_by('-fecha_publicacion')
    
class ResultadosView(generic.DetailView):
    model = Pregunta
    template_name = 'polls/resultado.html'

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
