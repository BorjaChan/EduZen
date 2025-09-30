from django.urls import path
from . import views

app_name = "materias"

urlpatterns = [
    path("", views.lista_materias, name="list"),         # Dashboard / listado principal
    path("actividades/", views.actividades, name="actividades"),
    path("seguimiento/", views.seguimiento, name="seguimiento"),
    path("reuniones/", views.reuniones, name="reuniones"),
]
