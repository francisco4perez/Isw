from django.conf.urls import url

from . import views

app_name = 'buscador'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^resultados/', views.resultados_view, name='resultados_view'),
]