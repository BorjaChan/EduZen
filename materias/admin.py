from django.contrib import admin
from .models import Materia

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ficha', 'docente')
    list_filter = ('ficha', 'docente')
    search_fields = ('nombre',)
    filter_horizontal = ('estudiantes',)
