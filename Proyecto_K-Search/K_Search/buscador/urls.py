from django.conf.urls import url

from . import views

app_name = 'buscador'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^resultados/', views.resultados_view, name='resultados_view'),
    url(r'^extraccion-contenidos/', views.extraccion_contenidos, name='extraccion_contenidos'),
    url(r'^paginas-de-confianza/', views.paginas_de_confianza, name='paginas_de_confianza'),
    url(r'^ver-contenidos/', views.ver_contenidos, name='ver_contenidos'),
]