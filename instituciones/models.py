from django.db import models
from django.conf import settings

class Institucion(models.Model):
    GRUPO_CHOICES = [
        ("fichas", "Fichas (SENA)"),
        ("grados", "Grados (Colegio)"),
        ("carreras", "Carreras (Universidad)"),
        ("grupos", "Grupos"),
        ("otros", "Otros"),
    ]

    MATERIA_CHOICES = [
        ("materias", "Materias"),
        ("asignaturas", "Asignaturas"),
        ("modulos", "Módulos"),
        ("cursos", "Cursos"),
        ("competencia", "Competencia"),
        ("otros", "Otros"),
    ]

    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    politica_retencion = models.TextField(blank=True, null=True)

    asignacion_grupo = models.CharField(
        max_length=20,
        choices=GRUPO_CHOICES,
        default="grupos",
    )

    asignacion_materia = models.CharField(
        max_length=20,
        choices=MATERIA_CHOICES,
        default="materias",
    )

    creado = models.DateTimeField(auto_now_add=True)

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instituciones_creadas"
    )

    def __str__(self):
        return self.nombre
