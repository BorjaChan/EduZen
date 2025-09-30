#El mapa de rutas específico para la app 'users'.
#Define las URLs que pertenecen a esta app (ej: '/login', '/registro').
from django.urls import path
from .views import CustomLoginView, student_register_view
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('registro/', student_register_view, name='register_student'),
    
]

