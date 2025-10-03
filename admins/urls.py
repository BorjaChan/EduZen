from django.urls import path
from . import views

app_name = "admins"

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="dashboard"),
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/<int:pk>/edit/", views.user_edit, name="user_edit"),
    path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),
    path("institucion/<int:pk>/", views.institution_detail, name="institution_detail"),
    path("instituciones/", views.institucion_list, name="institucion_list"),
    path("instituciones/create/", views.institucion_create, name="institucion_create"),
    path('institucion/<int:pk>/delete/', views.institucion_delete, name='institucion_delete'),

]
