from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='estudiante_dashboard'),
]