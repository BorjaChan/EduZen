# ¡Fundamental! Aquí defines la estructura de tu base de datos usando clases de Python.
# Cada clase en este archivo es una tabla en la base de datos. Son los "planos" de tus datos.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
   
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("estudiante", "Estudiante"),
        ("docente", "Docente"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="estudiante")
    ficha = models.ForeignKey('Ficha', null=True, blank=True, on_delete=models.SET_NULL)  # estudiante o docente
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def save(self, *args, **kwargs):
        # reglas de permisos según role
        if self.role == "admin":
            self.is_staff = True
            self.is_superuser = True
        elif self.role == "docente":
            self.is_staff = True   # puede entrar al admin si quieres
            self.is_superuser = False
        else:  # estudiante
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Ficha(models.Model):
    nombre = models.CharField(max_length=100)
    docentes = models.ManyToManyField('CustomUser', related_name='fichas_dictadas', blank=True, limit_choices_to={'role': 'docente'})

    def __str__(self):
        return self.nombre