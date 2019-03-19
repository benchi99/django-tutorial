from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # URL => /polls/
    path('', views.IndexView.as_view(), name='index'),
    # URL => /polls/{id}/
    # Tutorial 2
    # path('<int:id_pregunta>/', views.detalle, name='Detalle'),
    path('<int:pk>/', views.DetalleView.as_view(), name='Detalle'),
    # URL => /polls/{id}/resultados
    # Tutorial 2
    # path('<int:id_pregunta>/resultados/', views.resultados, name='Resultados'),
    path('<int:pk>/resultados/', views.ResultadosView.as_view(), name='Resultados'),
    # URL => /polls/id/voto
    path('<int:id_pregunta>/voto/', views.voto, name='Voto')
]
