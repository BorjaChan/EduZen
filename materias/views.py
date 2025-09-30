from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def lista_materias(request):
    return render(request, "materias/lista.html")  # plantilla que ya tenías

@login_required
def actividades(request):
    return render(request, "materias/actividades.html")

@login_required
def seguimiento(request):
    return render(request, "materias/seguimiento.html")

@login_required
def reuniones(request):
    return render(request, "materias/reuniones.html")
