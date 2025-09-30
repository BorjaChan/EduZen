# Aquí personalizas cómo se ven y funcionan los modelos en el panel de administrador (/admin).
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Ficha

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'role', 'ficha', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'ficha')}),  # <--- aquí ficha
        ('Roles y permisos', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'ficha', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
@admin.register(Ficha)
class FichaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    filter_horizontal = ('docentes',)

