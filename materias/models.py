from django.db import models
from users.models import CustomUser, Ficha

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE, related_name="materias")
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

    def __str__(self):
        return self.nombre
