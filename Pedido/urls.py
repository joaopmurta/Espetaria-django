from django.urls import path
from . import views

urlpatterns = [
    path('lancar_pedido/', views.lancar_pedido, name='lancar_pedido'),
    path('pedido/', views.pedidos, name='pedidos'),
]