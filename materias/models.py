from django.db import models
from users.models import CustomUser, Ficha
from django.conf import settings
from instituciones.models import Institucion

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE, related_name="materias")
    institucion = models.ForeignKey(
    "instituciones.Institucion",
    on_delete=models.CASCADE,
    related_name="materias",
    null=True,  
    blank=True
)
    docente = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'docente'},
        related_name="materias_dictadas"
    )
    estudiantes = models.ManyToManyField(
        CustomUser,
        blank=True,
        limit_choices_to={'role': 'estudiante'},
        related_name="materias_inscritas"
    )

class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to="actividades/", blank=True, null=True)
    fecha_entrega = models.DateField()
    completada = models.BooleanField(default=False)

    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'docente'},
        related_name="actividades"
    )
    materia = models.ForeignKey(  
        "materias.Materia",
        on_delete=models.CASCADE,
        related_name="actividades"
    )

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class Entrega(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="entregas")
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to="entregas/")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Entrega de {self.estudiante.email} para {self.actividad.titulo}"
