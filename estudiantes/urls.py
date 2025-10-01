from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("actividades/", views.actividades, name="actividades"),
    path("seguimiento/", views.seguimiento, name="seguimiento"),
    path("reuniones/", views.reuniones, name="reuniones"),
]
