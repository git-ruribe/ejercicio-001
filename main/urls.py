from django.urls import path

from . import views

urlpatterns = [
    #path('', views.bienvenida, name='main'),
    # ex: /polls/5/
    path('equipo/<int:encuentro_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:encuentro_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:encuentro_id>/vote/', views.vote, name='vote'),
    # ex: /polls/5/vote/
    path('equipos/', views.equipos, name='equipos'),
    # path('', views.equipos, name='principal'),
    path('jornada/<int:jornada_id>', views.jornada, name='jornada'),
    path('', views.inicio, name='inicio'),
    path('pronostico/', views.pronosticar, name='pronosticar'),  
]
