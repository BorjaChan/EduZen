# El "cerebro" de tu aplicación.
# Cada función o clase aquí maneja la lógica de lo que sucede cuando un usuario visita una URL.
# Recibe la petición del usuario, interactúa con los modelos (si es necesario) y devuelve una respuesta (generalmente una plantilla HTML).
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required



class CustomLoginView(LoginView):
    template_name = 'users/login_form.html'  # tu formulario de login personalizado

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Si ya está logueado, manda al dashboard
        return super().dispatch(request, *args, **kwargs)

def student_register_view(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']  
            user.last_name = form.cleaned_data['last_name']   
            user.ficha = form.cleaned_data['ficha']  
            user.role = 'estudiante'
            user.save()
            return redirect('login')
    else:
        form = StudentRegisterForm()

    return render(request, 'users/register.html', {'form': form})

