from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("acerca-de", views.acerca_de, name="acerca_de"),
    path("cursos", views.cursos, name="cursos"),
    path("nuevo_index", views.nuevo_index, name="index_render"),
    path("servicio", views.servicio, name="servicio"),
    path("dolar", views.dolar, name="dolar"),
    path("dolar_vista", views.dolar_vista, name="dolar_vista"),
    path("aeropuertos", views.aeropuertos, name="aeropuertos"),
    path("dolar_render", views.dolar_render, name="dolar_render"),
    path("cursos_render", views.cursos_render, name="cursos_render"),
    path("curso/<str:nombre_curso>", views.curso, name="curso"),
    path("nuevo-curso", views.nuevo_curso, name="nuevo_curso"),
    path("modelos", views.modelos, name="modelos")
]
