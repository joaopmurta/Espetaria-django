from .models import Pedido


def contar_pedidos_por_status():
    pedidos = Pedido.objects.all()
    return {
        'Em espera': pedidos.filter(status='Em espera').count(),
        'Em Preparo': pedidos.filter(status='Em Preparo').count(),
        'Pronto': pedidos.filter(status='Pronto').count(),
        'Entregue': pedidos.filter(status='Entregue').count(),
    }
