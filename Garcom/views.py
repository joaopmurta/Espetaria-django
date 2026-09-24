from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#   Só entra aqui quem estiver autenticado
@login_required 
def home_screen(request):
    return render(request, 'garcom/home_screen.html')