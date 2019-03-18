from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # URL => /polls/
    path('', views.index, name='index'),
    # URL => /polls/{id}/
    path('<int:id_pregunta>/', views.detalle, name='Detalle'),
    # URL => /polls/{id}/resultados
    path('<int:id_pregunta>/resultados/', views.resultados, name='Resultados'),
    # URL => /polls/id/voto
    path('<int:id_pregunta>/voto/', views.voto, name='Voto')
]
