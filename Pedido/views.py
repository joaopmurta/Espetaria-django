from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from .models import Pedido, ItemPedido
from .forms import PedidoForm, ItemPedidoForm
from django.utils import timezone
from datetime import timedelta

from Garcom.models import Garcom 

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
            
            # Busca crachá do garçom no banco de dados
            garcom_logado = Garcom.objects.get(usuario=request.user)
            
            novo_pedido.garcom = garcom_logado
            novo_pedido.status = 'Em espera'  # Define o status inicial do pedido
            novo_pedido.save() 
            
            # Liga os espetos à mesa salva e guardamos tudo
            formset_itens.instance = novo_pedido
            formset_itens.save()
            
            return redirect('home')
            
    else:
        form_pedido = PedidoForm()
        formset_itens = ItemPedidoFormSet()
        
    return render(request, 'pedidos/lancar_pedido.html', {
        'form_pedido': form_pedido, 
        'formset_itens': formset_itens
    })


@login_required
def pedidos(request):
    if(request.method == 'GET'):
        pedidos = Pedido.objects.all()
        pedido_status = request.GET.get('status', None)

        if(pedido_status is None): # None é um tipo especial do Python, nao uma palavra

            return render(request, 'pedidos/pedidos.html', {
                'pedidos': pedidos.filter(status = 'Em Preparo'), # Django não reconhece is
            })

        elif(pedido_status != 'todos'):
            return render(request, 'pedidos/pedidos.html', {
                'pedidos': pedidos.filter(status=pedido_status),
            })
        
    return render(request, 'pedidos/pedidos.html', {
        'pedidos': pedidos,
    })

def filter_by_table(request):
    if request.method == 'GET':
        mesa = request.GET.get('mesa', None)
        pedidos = Pedido.objects.all()

        if mesa is None:
            pedidos = Pedido.objects.none() # Melhor que usar []
        elif(mesa.isdigit()):
            pedidos = pedidos.filter(mesa=int(mesa))

    return render(request, 'pedidos/pedidos.html', {
        'pedidos': pedidos,
    })

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
@login_required
def notificar_hud():
    pedidos = Pedido.objects.all()
    espera_count = pedidos.filter(status='Em espera').count()
    preparo_count = pedidos.filter(status='Em Preparo').count()
    pronto_count = pedidos.filter(status='Pronto').count()
    entregue_count = pedidos.filter(status='Entregue').count()
    # Define o tempo limite para pedidos críticos
    
    # Acha a hora exata de "20 minutos atrás"
    limite_atraso = timezone.now() - timedelta(minutes=20)
    # Acha a hora exata de "10 minutos atrás"
    limite_critico = timezone.now() - timedelta(minutes=10)

    #count_atraso = pedidos.filter(status='Em Preparo' or status='Em espera', criado_em__lt=limite_atraso).count()
    #count_critico = pedidos.filter(status='Em Preparo' or status='Em espera', criado_em__lt=limite_critico).count()
    count_atraso = pedidos.filter(status__in=['Em espera', 'Em preparo'], criado_em__lt=limite_atraso).count()
    count_critico = pedidos.filter(status__in=['Em espera', 'Em preparo'], criado_em__lt=limite_critico, criado_em__gte=limite_atraso).count()

    count_by_status = {
        'Em espera': espera_count,
        'Em Preparo': preparo_count,
        'Pronto': pronto_count,
        'Entregue': entregue_count,
    }
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "Espetaria",
        {
            "type": "send_update",
            "count_by_status": count_by_status
        }
    )

@login_required
def atualizar_status_pedido(request, pedido_id, novo_status):
    pedido = Pedido.objects.get(id=pedido_id)
    
    user_group = request.user.groups.first()
    
    if (user_group.name == 'Churrasqueiro' and novo_status in ['Em Preparo', 'Pronto']) or (user_group.name == 'Garcom' and novo_status == 'Entregue'):
        pedido.status = novo_status
        pedido.save()
    
    notificar_hud()
    return redirect('pedidos')
