from django.db import models
from Garcom.models import Garcom
from Espeto.models import Espeto 
from Mesa.models import Mesa

# Etapas do pedido
ETAPAS_PEDIDO = [
    ('Em espera', 'Em Espera'),
    ('Em Preparo', 'Em Preparo'),
    ('Pronto', 'Pronto'),
    ('Entregue', 'Entregue'),
]


class Pedido(models.Model):
    garcom = models.ForeignKey(Garcom, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    #mesa = models.IntegerField()  # Alterado para IntegerField para armazenar apenas o número da mesa
    status = models.CharField(max_length=50, choices=ETAPAS_PEDIDO, blank=True, null=True)
    # auto_now_add=True preenche a hora automaticamente no momento em que o pedido é salvo
    criado_em = models.DateTimeField(auto_now_add=True) 

    @property # @property já cria automaticamente o atributo is_manager para cada pedido
    def is_manager(self):
        return self.garcom.usuario.groups.filter(name='Gerente').exists()

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero}"

# Pontos da carne para o espeto, com opções de escolha
OPCOES_PONTO = [
    ('Mal passado', 'Mal passado'),
    ('Ao ponto', 'Ao ponto'),
    ('Bem passado', 'Bem passado'),
    ('Não se aplica', 'Não se aplica')
]

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    espeto = models.ForeignKey(Espeto, on_delete=models.CASCADE) 
    
    # Adicionamos o parâmetro 'choices' aqui:
    ponto = models.CharField(max_length=50, choices=OPCOES_PONTO, blank=True, null=True)

    def __str__(self):
        return f"{self.espeto} (Pedido #{self.pedido.id})"