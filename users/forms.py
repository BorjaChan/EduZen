#Aquí defines los formularios de Django.
#Facilita la creación y validación de formularios HTML, como el de registro o contacto.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Ficha
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class StudentRegisterForm(UserCreationForm):
    ficha = forms.ModelChoiceField(
        queryset=Ficha.objects.all(),
        empty_label="Seleccione una ficha",
        label="Ficha"
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'ficha', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'ficha': 'Ficha',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name')
        if ' ' in nombre:
            raise forms.ValidationError("El campo Nombres no debe contener espacios.")
        return nombre

    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name')
        if ' ' in apellido:
            raise forms.ValidationError("El campo Apellidos no debe contener espacios.")
        return apellido

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ' ' in email:
            raise forms.ValidationError("El correo no debe contener espacios.")
        return email

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'ficha', 'password1', 'password2']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'role': 'Rol',
            'ficha': 'Ficha (solo estudiantes)',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })


class CustomUserChangeForm(UserChangeForm):
    password = None  # ocultamos campo de password en edición

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'ficha']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'role': 'Rol',
            'ficha': 'Ficha (solo estudiantes)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

