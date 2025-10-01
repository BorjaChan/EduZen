from django.urls import path
from . import views

app_name = "docentes"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("crear/", views.crear, name="crear"),
    
]
