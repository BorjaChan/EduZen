from django import forms
from .models import Institucion

class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = ["nombre", "descripcion", "politica_retencion", "asignacion_grupo", "asignacion_materia"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "politica_retencion": forms.Textarea(attrs={"rows": 3}),
        }
