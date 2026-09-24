from django.db import models

# Create your models here.
class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidade = models.IntegerField()

    def __str__(self):
        return f"Mesa {self.numero} - Capacidade: {self.capacidade}"