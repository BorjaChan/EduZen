from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.forms import CustomUserCreationForm, CustomUserChangeForm  # asegúrate que existan
from .decorators import admin_required   # 👈 importamos nuestro decorador

User = get_user_model()  # Tu modelo de usuario personalizado (CustomUser)


@login_required
@admin_required
def admin_dashboard(request):
    return render(request, "admins/dashboard.html")


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
