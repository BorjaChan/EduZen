from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Course, Subject

User = get_user_model()

class AdminUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "role", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombres"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellidos"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electrónico"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }

class AdminUserEditForm(UserChangeForm):
    password = None  # para ocultar el campo de contraseña
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "role"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Grado Sexto / Ficha 2959811"})
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["nombre", "curso", "docente"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Matemáticas"}),
            "curso": forms.Select(attrs={"class": "form-control"}),
            "docente": forms.Select(attrs={"class": "form-control"}),
        }

