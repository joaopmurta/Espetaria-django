from django.db import models
from django.contrib.auth.models import User

class Churrasqueiro(models.Model):
    # O OneToOneField liga este perfil diretamente ao sistema de login do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username