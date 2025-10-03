from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from materias.models import Materia
from materias.forms import MateriaForm


@login_required
def dashboard(request):
    institucion = request.user.institucion
    materias = Materia.objects.filter(
        docente=request.user,
        institucion=institucion
    )
    return render(request, "docentes/dashboard.html", {"materias": materias})


@login_required
def crear(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.docente = request.user
            materia.institucion = request.user.institucion  # filtro institucional
            materia.save()
            messages.success(request, f"La materia {materia.nombre} fue creada correctamente.")
            return redirect("docentes:dashboard")
    else:
        form = MateriaForm()

    return render(request, "docentes/crear.html", {"form": form})


@login_required
def detalle(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    if request.user.institucion and materia.institucion != request.user.institucion:
        return HttpResponseForbidden("No puedes acceder a materias de otra institución.")

    return render(request, "docentes/detalle.html", {"materia": materia})
