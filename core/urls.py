# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "core" 

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
