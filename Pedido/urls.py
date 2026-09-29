from django.urls import path
from . import views

urlpatterns = [
    path('lancar_pedido/', views.lancar_pedido, name='lancar_pedido'),
    path('pedido/', views.pedidos, name='pedidos'),
    path('pedido/edit_status/<int:pedido_id>/<str:novo_status>/', views.atualizar_status_pedido, name='atualizar_status_pedido'), # str nao String
]