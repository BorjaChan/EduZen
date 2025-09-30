from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "students/dashboard.html")

@login_required
def actividades(request):
    return render(request, "students/actividades.html")

@login_required
def seguimiento(request):
    return render(request, "students/seguimiento.html")

@login_required
def reuniones(request):
    return render(request, "students/reuniones.html")
