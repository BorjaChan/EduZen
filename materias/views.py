from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import ActividadForm, MateriaForm, EntregaForm
from .models import Actividad, Entrega, Materia


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
    institucion = request.user.institucion
    if not institucion:
        return render(request, "materias/lista_actividades.html", {"actividades": Actividad.objects.none()})

    if request.user.role == "estudiante":
        actividades = Actividad.objects.filter(
            materia__ficha=request.user.ficha,
            materia__ficha__institucion=institucion
        )
    elif request.user.role == "docente":
        actividades = Actividad.objects.filter(
            docente=request.user,
            materia__ficha__institucion=institucion
        )
    else:
        actividades = Actividad.objects.none()

    return render(request, "materias/lista_actividades.html", {"actividades": actividades})


@login_required
def mis_materias(request):
    institucion = request.user.institucion
    if not institucion:
        return render(request, "materias/mis_materias.html", {"materias": Materia.objects.none()})

    if request.user.role == "estudiante":
        materias = request.user.materias_inscritas.filter(
            ficha=request.user.ficha,
            ficha__institucion=institucion
        )
    elif request.user.role == "docente":
        materias = request.user.materias_dictadas.filter(
            ficha__institucion=institucion
        )
    else:
        materias = Materia.objects.none()

    return render(request, "materias/mis_materias.html", {"materias": materias})


def detalle_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    # asegurar que la materia pertenece a la institución del usuario
    if request.user.institucion and materia.ficha.institucion != request.user.institucion:
        return HttpResponseForbidden("No tienes acceso a esta materia.")

    actividades = materia.actividades.all().order_by("-creado")

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

            # asegurar institución desde el docente
            if materia.ficha and materia.ficha.institucion != request.user.institucion:
                return HttpResponseForbidden("No puedes crear una materia fuera de tu institución.")

            materia.save()
            return redirect("materias:list")
    else:
        form = MateriaForm()

    return render(request, "materias/crear_materia.html", {"form": form})


@login_required
def crear_actividad(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    # validar institución
    if request.user.institucion and materia.ficha.institucion != request.user.institucion:
        return HttpResponseForbidden("No tienes acceso a esta materia.")

    if request.user == materia.docente:
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

    # validar institución
    if request.user.institucion and actividad.materia.ficha.institucion != request.user.institucion:
        return HttpResponseForbidden("No tienes acceso a esta actividad.")

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

    # validar institución
    if request.user.institucion and materia.ficha.institucion != request.user.institucion:
        return HttpResponseForbidden("No tienes acceso a esta materia.")

    if request.user != materia.docente:
        return HttpResponseForbidden("No tienes permiso para eliminar esta materia.")

    if request.method == "POST":
        materia.delete()
        messages.success(request, "La materia fue eliminada correctamente.")
        return redirect("materias:mis_materias")

    return render(request, "materias/eliminar_materia.html", {"materia": materia})
