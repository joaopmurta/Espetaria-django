"""
ASGI config for crud project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter 
import Pedido.routing # Routes file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(
        Pedido.routing.websocket_urlpatterns # Lista de rotas
    )
})