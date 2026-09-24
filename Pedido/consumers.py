import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync # Para chamar funções assíncronas de dentro de funções síncronas (Garçons e churrasqueiro formam um "grupo" de trabalho, e o Django precisa de um "coordenador" para organizar a comunicação entre eles)


class PedidoHUDConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("Espetaria", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("Espetaria", self.channel_name) # group_discard é o oposto de group_add, ou seja, remove o canal do grupo
        pass

    def receive(self, pedidos): # Cliente manda dados para o servidor e o server RECEBE
        data = json.loads(pedidos) # Recebe os dados do cliente e transforma em um dicionário Python

        self.send(text_data=json.dumps({
            'message': 'Dados recebidos com sucesso!',
            'data': data
        }))

    def send_update(self, event): # Servidor manda dados para o cliente e o cliente RECEBE
        data = event['count_by_status'] # O servidor envia um dicionário com a contagem de pedidos por status, e o cliente recebe esse dicionário e atualiza a HUD

        self.send(text_data=json.dumps({
            'message': 'Atualização recebida com sucesso!',
            'data': data
        }))