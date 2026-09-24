from django.db import models

class Espeto (models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.nome} - {self.tipo}"