from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    role = request.user.role.lower()

    if role == "docente":
        return render(request, "docentes/dashboard.html")
    elif role == "estudiante":
        return render(request, "estudiantes/dashboard.html")
    else:
        return render(request, "dashboard/dashboard.html")
