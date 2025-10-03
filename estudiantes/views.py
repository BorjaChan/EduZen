from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from materias.models import Materia, Actividad, Entrega
from users.models import CustomUser, Ficha


@login_required
def dashboard(request):
    user = request.user
    institucion = user.institucion

    if user.role == "estudiante":
        actividades = Actividad.objects.filter(
            materia__ficha=user.ficha,
            institucion=institucion
        ).order_by('-fecha_entrega')
    elif user.role == "docente":
        actividades = Actividad.objects.filter(
            docente=user,
            institucion=institucion
        ).order_by('-fecha_entrega')
    else:
        actividades = Actividad.objects.none()

    total_materias = Materia.objects.filter(
        ficha=user.ficha,
        institucion=institucion
    ).count()
    entregas = Entrega.objects.filter(estudiante=user)

    completadas = entregas.count()
    pendientes = actividades.count() - completadas

    # marcar estado dinámico
    for act in actividades:
        if act.entregas.filter(estudiante=user).exists():
            act.estado = "completado"
        else:
            act.estado = "pendiente"

    ultimas_actividades = actividades[:5]

    context = {
        "total_materias": total_materias,
        "pendientes": pendientes,
        "completadas": completadas,
        "ultimas_actividades": ultimas_actividades,
    }
    return render(request, "estudiantes/dashboard.html", context)


@login_required
def lista_estudiantes(request):
    institucion = request.user.institucion
    estudiantes = CustomUser.objects.filter(
        role="estudiante",
        institucion=institucion
    ) if institucion else CustomUser.objects.none()

    return render(request, "estudiantes/lista.html", {"estudiantes": estudiantes})


@login_required
def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(CustomUser, pk=pk, role="estudiante")

    if request.user.institucion and estudiante.institucion != request.user.institucion:
        return HttpResponseForbidden("No tienes acceso a este estudiante.")

    return render(request, "estudiantes/detalle.html", {"estudiante": estudiante})


@login_required
def asignar_ficha(request, estudiante_id):
    estudiante = get_object_or_404(CustomUser, pk=estudiante_id, role="estudiante")

    if request.user.institucion and estudiante.institucion != request.user.institucion:
        return HttpResponseForbidden("No puedes modificar estudiantes de otra institución.")

    if request.method == "POST":
        ficha_id = request.POST.get("ficha_id")
        ficha = get_object_or_404(Ficha, pk=ficha_id)

        if request.user.institucion and ficha.institucion != request.user.institucion:
            return HttpResponseForbidden("No puedes asignar fichas de otra institución.")

        estudiante.ficha = ficha
        estudiante.save()
        messages.success(
            request,
            f"Se asignó la ficha {ficha.nombre} a {estudiante.first_name} {estudiante.last_name}."
        )
        return redirect("estudiantes:detalle", pk=estudiante.pk)

    fichas = Ficha.objects.filter(
        institucion=request.user.institucion
    ) if request.user.institucion else Ficha.objects.none()

    return render(request, "estudiantes/asignar_ficha.html", {
        "estudiante": estudiante,
        "fichas": fichas
    })
