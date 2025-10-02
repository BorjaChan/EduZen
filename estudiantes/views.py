from django.shortcuts import render
from materias.models import Materia, Actividad, Entrega
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user

    if user.role == "estudiante":
        actividades = Actividad.objects.filter(materia__ficha=user.ficha).order_by('-fecha_entrega')
    elif user.role == "docente":
        actividades = Actividad.objects.filter(docente=user).order_by('-fecha_entrega')
    else:
        actividades = Actividad.objects.none()

    total_materias = Materia.objects.filter(ficha=user.ficha).count()
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

