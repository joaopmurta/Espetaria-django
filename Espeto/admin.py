from django.contrib import admin
from .models import Espeto # Importar o modelo

# Registrar o modelo no painel
admin.site.register(Espeto)