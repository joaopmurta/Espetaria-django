from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/hud/', consumers.PedidoHUDConsumer.as_asgi())
]