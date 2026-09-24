from django.urls import path
from . import views # Importar as views
import Garcom.views # Importar as views do app Pedido

urlpatterns = [
   path('update_espeto/<int:id>', views.editar_espeto, name = 'editar_espeto'),
   path('delete_espeto/<int:id>', views.deletar_espeto, name = 'deletar_espeto'), 
   path('create_espeto/', views.adicionar_espeto, name = 'adicionar_espeto'), 
   path('painel_espetos/', views.painel_espetos, name = 'painel_espetos'),
   path('garcom/home_screen/', Garcom.views.home_screen, name = 'garcom/home_screen')
]