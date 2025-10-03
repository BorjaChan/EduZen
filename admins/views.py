from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.forms import CustomUserCreationForm, CustomUserChangeForm  
from .decorators import admin_required   
from instituciones.models import Institucion
from instituciones.forms import InstitucionForm

User = get_user_model()  


@login_required
@admin_required
def admin_dashboard(request):
    instituciones = Institucion.objects.all()

   
    data = []
    for inst in instituciones:
        data.append({
            "id": inst.id,
            "nombre": inst.nombre,
            "total_usuarios": inst.usuarios.count(),   
            "total_materias": inst.materias.count(),
            "total_fichas": inst.fichas.count(),
        })

    return render(request, "admins/dashboard.html", {
        "instituciones": data,
    })


@login_required
@admin_required
def institution_detail(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    materias = institucion.materias.all()
    fichas = institucion.fichas.all()
    usuarios = institucion.usuarios.all()

    return render(request, "admins/institution_detail.html", {
        "institucion": institucion,
        "materias": materias,
        "fichas": fichas,
        "usuarios": usuarios,
    })

@login_required
@admin_required
def user_list(request):
    users = User.objects.all()
    return render(request, "admins/users/list.html", {"users": users})


@login_required
@admin_required
def user_create(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admins:user_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "admins/users/form.html", {"form": form})


@login_required
@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("admins:user_list")
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, "admins/users/form.html", {"form": form})


@login_required
@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("admins:user_list")
    return render(request, "admins/users/delete.html", {"user": user})

def institucion_list(request):
    instituciones = Institucion.objects.all()
    return render(request, "admins/instituciones/list.html", {"instituciones": instituciones})

@login_required
@admin_required
def institucion_create(request):
    if request.method == "POST":
        form = InstitucionForm(request.POST)
        if form.is_valid():
            institucion = form.save(commit=False)
            institucion.creado_por = request.user  #admin la crea
            institucion.save()
            return redirect("admins:institucion_list")
    else:
        form = InstitucionForm()
    return render(request, "admins/instituciones/create.html", {"form": form})

def institucion_delete(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    institucion.delete()
    return redirect('admins:institucion_list')