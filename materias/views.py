from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import ActividadForm
from .models import Actividad, Entrega
from .models import Materia
from .forms import MateriaForm, ActividadForm, EntregaForm

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

@login_required
def crear_actividad(request):
    if request.user.role != "docente":
        return redirect("dashboard") 

    if request.method == "POST":
        form = ActividadForm(request.POST, request.FILES)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.docente = request.user
            actividad.save()
            return redirect("materias:actividades") 
    else:
        form = ActividadForm()

    return render(request, "materias/crear_actividad.html", {"form": form})

@login_required
def lista_actividades(request):
    if request.user.role == "estudiante":
        actividades = Actividad.objects.filter(materia__ficha=request.user.ficha)
    elif request.user.role == "docente":
        actividades = Actividad.objects.filter(docente=request.user)
    else:
        actividades = Actividad.objects.none()

    return render(request, "materias/lista_actividades.html", {"actividades": actividades})

@login_required
def mis_materias(request):
    if request.user.role == "estudiante":
        materias = Materia.objects.filter(ficha=request.user.ficha)
    elif request.user.role == "docente":
        materias = Materia.objects.filter(docente=request.user)
    else:
        materias = Materia.objects.none()

    return render(request, "materias/mis_materias.html", {"materias": materias})


def detalle_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    actividades = materia.actividades.all().order_by("-creado")  # relacionadas al modelo Actividad

    return render(request, "materias/detalle_materia.html", {
        "materia": materia,
        "actividades": actividades,
    })

@login_required
def crear_materia(request):
    if request.user.role != "docente":
        return HttpResponseForbidden("Solo los docentes pueden crear materias.")

    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.docente = request.user  
            materia.save()
            return redirect("materias:list")  
    else:
        form = MateriaForm()

    return render(request, "materias/crear_materia.html", {"form": form})

@login_required
def crear_actividad(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.user == materia.docente:  # solo docente
        if request.method == "POST":
            form = ActividadForm(request.POST)
            if form.is_valid():
                actividad = form.save(commit=False)
                actividad.materia = materia
                actividad.docente = request.user
                actividad.save()
                return redirect("materias:detalle", pk=materia.pk)
        else:
            form = ActividadForm()
        return render(request, "materias/crear_actividad.html", {"form": form, "materia": materia})
    else:
        return redirect("materias:detalle", pk=materia.pk)


@login_required
def entregar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    if request.method == "POST":
        form = EntregaForm(request.POST, request.FILES)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.actividad = actividad
            entrega.estudiante = request.user
            entrega.save()
            return redirect("materias:detalle", pk=actividad.materia.pk)
    else:
        form = EntregaForm()
    return render(request, "materias/entregar_actividad.html", {"form": form, "actividad": actividad})

@login_required
def eliminar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    
    if request.user != materia.docente:
        return HttpResponseForbidden("No tienes permiso para eliminar esta materia.")

    if request.method == "POST":
        materia.delete()
        messages.success(request, "La materia fue eliminada correctamente.")
        return redirect("materias:mis_materias") 

    return render(request, "materias/eliminar_materia.html", {"materia": materia})