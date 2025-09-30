from django.db import models

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
        ("otros", "Otros"),
    ]

    nombre = models.CharField(max_length=255, unique=True)
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

    def __str__(self):
        return self.nombre
