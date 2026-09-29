from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Espeto.models import Espeto
from Garcom.models import Garcom
from Mesa.models import Mesa
from .models import ItemPedido, Pedido


class PedidoListFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='equipe', password='teste123')
        self.garcom = Garcom.objects.create(usuario=self.user)
        self.mesa_um = Mesa.objects.create(numero=1, capacidade=4)
        self.mesa_dois = Mesa.objects.create(numero=2, capacidade=2)
        self.espeto = Espeto.objects.create(nome='Alcatra', tipo='Bovino', preco='12.50')
        self.pedido_espera = Pedido.objects.create(
            garcom=self.garcom,
            mesa=self.mesa_um,
            status='Em espera',
        )
        self.pedido_preparo = Pedido.objects.create(
            garcom=self.garcom,
            mesa=self.mesa_dois,
            status='Em Preparo',
        )
        ItemPedido.objects.create(
            pedido=self.pedido_espera,
            espeto=self.espeto,
            ponto='Ao ponto',
        )
        self.client.force_login(self.user)

    def test_filters_status_and_table_together(self):
        response = self.client.get(reverse('pedidos'), {
            'status': 'Em espera',
            'mesa': str(self.mesa_um.pk),
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['pedidos']), [self.pedido_espera])
        self.assertEqual(response.context['filtered_status'], 'Em espera')
        self.assertEqual(response.context['mesa'], str(self.mesa_um.pk))
        self.assertContains(response, 'Alcatra')

    def test_default_filter_shows_orders_in_preparation(self):
        response = self.client.get(reverse('pedidos'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['pedidos']), [self.pedido_preparo])

    def test_all_statuses_can_be_shown_for_a_table(self):
        response = self.client.get(reverse('pedidos'), {
            'status': 'todos',
            'mesa': str(self.mesa_um.pk),
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['pedidos']), [self.pedido_espera])
