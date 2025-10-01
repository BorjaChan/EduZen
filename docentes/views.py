from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from materias.models import Materia
from materias.forms import MateriaForm

@login_required
def dashboard(request):
    return render(request, "docentes/dashboard.html")
@login_required
def crear(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.docente = request.user 
            materia.save()
            return redirect("docentes:dashboard")
    else:
        form = MateriaForm()

    return render(request, "docentes/crear.html", {"form": form})