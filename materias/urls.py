from django.urls import path
from . import views

app_name = "materias"

urlpatterns = [
    path("", views.mis_materias, name="mis_materias"), 
    path("<int:pk>/", views.detalle_materia, name="detalle"),  
    path("actividades/", views.actividades, name="actividades"),
    path("seguimiento/", views.seguimiento, name="seguimiento"),
    path("reuniones/", views.reuniones, name="reuniones"),
    path("actividades/lista/", views.lista_actividades, name="lista_actividades"),
    path("actividades/nueva/", views.crear_actividad, name="crear_actividad"),
    path("", views.lista_materias, name="list"),
    path("nueva/", views.crear_materia, name="crear_materia"),
    path("<int:pk>/crear-actividad/", views.crear_actividad, name="crear_actividad"),
    path("actividad/<int:actividad_id>/entregar/", views.entregar_actividad, name="entregar_actividad"),
    path("materia/<int:pk>/eliminar/", views.eliminar_materia, name="eliminar_materia"),
]
