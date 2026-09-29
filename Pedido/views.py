from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from Garcom.models import Garcom
from Mesa.models import Mesa
from .forms import ItemPedidoForm, PedidoForm
from .models import ETAPAS_PEDIDO, ItemPedido, Pedido
from .services import contar_pedidos_por_status

ItemPedidoFormSet = inlineformset_factory(
    Pedido, ItemPedido, form=ItemPedidoForm, extra=1, can_delete=False
)


@login_required
def lancar_pedido(request):
    if request.method == 'POST':
        form_pedido = PedidoForm(request.POST)
        formset_itens = ItemPedidoFormSet(request.POST)

        if form_pedido.is_valid() and formset_itens.is_valid():
            novo_pedido = form_pedido.save(commit=False)
            novo_pedido.garcom = Garcom.objects.get(usuario=request.user)
            novo_pedido.status = 'Em espera'
            novo_pedido.save()

            formset_itens.instance = novo_pedido
            formset_itens.save()
            notificar_hud()
            return redirect('home')
    else:
        form_pedido = PedidoForm()
        formset_itens = ItemPedidoFormSet()

    return render(request, 'pedidos/lancar_pedido.html', {
        'form_pedido': form_pedido,
        'formset_itens': formset_itens,
        'mesas': Mesa.objects.order_by('numero'),
    })


@login_required
def pedidos(request):
    status = request.GET.get('status', 'Em Preparo')
    mesa = request.GET.get('mesa', '')
    status_validos = {valor for valor, _ in ETAPAS_PEDIDO}
    if status != 'todos' and status not in status_validos:
        status = 'Em Preparo'

    pedidos_filtrados = (
        Pedido.objects.select_related('mesa', 'garcom__usuario')
        .prefetch_related('itempedido_set__espeto')
        .order_by('-criado_em')
    )
    if status != 'todos':
        pedidos_filtrados = pedidos_filtrados.filter(status=status)
    if mesa.isdigit():
        pedidos_filtrados = pedidos_filtrados.filter(mesa_id=int(mesa))
    else:
        mesa = ''

    return render(request, 'pedidos/pedidos.html', {
        'pedidos': pedidos_filtrados,
        'filtered_status': status,
        'mesa': mesa,
        'mesas': Mesa.objects.order_by('numero'),
        'status_choices': ETAPAS_PEDIDO,
    })


def notificar_hud():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'Espetaria',
        {
            'type': 'send_update',
            'count_by_status': contar_pedidos_por_status(),
        },
    )


@login_required
def atualizar_status_pedido(request, pedido_id, novo_status):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    grupos = set(request.user.groups.values_list('name', flat=True))
    is_churrasqueiro = 'Churrasqueiro' in grupos or request.user.is_superuser
    is_garcom = 'Garcom' in grupos

    if (
        is_churrasqueiro and novo_status in ('Em Preparo', 'Pronto')
    ) or (
        is_garcom and novo_status == 'Entregue'
    ):
        pedido.status = novo_status
        pedido.save(update_fields=['status'])
        notificar_hud()

    return redirect('pedidos')
