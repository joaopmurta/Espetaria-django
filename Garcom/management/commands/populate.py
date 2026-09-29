from random import choice
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from Mesa.models import Mesa
from Espeto.models import Espeto
from Garcom.models import Garcom
from Churrasqueiro.models import Churrasqueiro

class Command(BaseCommand):
    help = 'Popula o banco de dados com mesas, espetos e funcionários'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando a população do banco de dados... 🚀")


        # 3. Criar as 10 Mesas 🪑
        for i in range(1, 11):
            Mesa.objects.get_or_create(
                numero=i,
                defaults={'capacidade': choice([2, 4, 6, 8])}  # Capacidade aleatória entre 2, 4, 6 ou 8
            )
        self.stdout.write("10 Mesas criadas no salão.")

        # 4. Criar o Cardápio de Espetos 🥩
        espetos_dados = [
            {"nome": "Picanha", "tipo": "Carne Bovina", "preco": 16.00},
            {"nome": "Alcatra", "tipo": "Carne Bovina", "preco": 12.00},
            {"nome": "Lombo", "tipo": "Carne Suína", "preco": 10.00},
            {"nome": "Filé de Frango", "tipo": "Frango", "preco": 10.00},
            {"nome": "Brochete", "tipo": "Misto", "preco": 14.00},
            {"nome": "Medalhão de Frango", "tipo": "Frango com Bacon", "preco": 13.00},
            {"nome": "Almôndega com Queijo", "tipo": "Carne Bovina", "preco": 14.00},
            {"nome": "Kafta", "tipo": "Carne Bovina", "preco": 12.00},
            {"nome": "Kafta Recheada", "tipo": "Carne Bovina", "preco": 15.00},
            {"nome": "Muçarela", "tipo": "Queijo", "preco": 11.00},
            {"nome": "Queijo Coalho com Mel", "tipo": "Queijo", "preco": 13.00},
            {"nome": "Aipim com Alho Poró", "tipo": "Vegetariano", "preco": 9.00},
            {"nome": "Almôndega de Grão de Bico (c/ Banana)", "tipo": "Vegano", "preco": 12.00},
            {"nome": "Coração", "tipo": "Miúdos", "preco": 11.00},
            {"nome": "Linguicinha", "tipo": "Suíno", "preco": 9.00},
            {"nome": "Pão de Alho", "tipo": "Acompanhamento", "preco": 8.00},
            {"nome": "Costela Bovina", "tipo": "Carne Bovina", "preco": 14.00},
            {"nome": "Cupim", "tipo": "Carne Bovina", "preco": 14.00},
            {"nome": "Salsichão", "tipo": "Misto", "preco": 8.00},
            {"nome": "Abobrinha com Parmesão", "tipo": "Vegetariano", "preco": 9.00},
        ]

        for dado in espetos_dados:
            Espeto.objects.get_or_create(
                nome=dado['nome'], 
                defaults={'tipo': dado['tipo'], 'preco': dado['preco']}
            )
        self.stdout.write("Cardápio de 20 espetos atualizado.")

        self.stdout.write(self.style.SUCCESS('✨ Banco populado com sucesso!'))