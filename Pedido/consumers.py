import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .services import contar_pedidos_por_status


class PedidoHUDConsumer(WebsocketConsumer):
    def connect(self):
        if not self.scope['user'].is_authenticated:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)("Espetaria", self.channel_name)
        self.accept()
        self.send(text_data=json.dumps({
            'count_by_status': contar_pedidos_por_status(),
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("Espetaria", self.channel_name)

    def receive(self, pedidos):
        data = json.loads(pedidos)
        self.send(text_data=json.dumps({
            'message': 'Dados recebidos com sucesso!',
            'data': data,
        }))

    def send_update(self, event):
        self.send(text_data=json.dumps({
            'count_by_status': event['count_by_status'],
        }))
