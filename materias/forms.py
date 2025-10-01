from django import forms
from .models import Actividad, Entrega
from .models import Materia

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["titulo", "descripcion", "archivo", "fecha_entrega", "materia"]

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ["nombre", "descripcion", "ficha"] 
        labels = {
            "nombre": "Nombre de la materia",
            "descripcion": "Descripción",
            "ficha": "Ficha / Grupo",
        }

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ["archivo"]