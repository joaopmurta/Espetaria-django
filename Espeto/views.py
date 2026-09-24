from django.shortcuts import render, redirect
from .models import Espeto  # Importa o modelo para a View saber o que é um Espeto
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def painel_espetos(request):
    todos_espetos = Espeto.objects.all()

    return render(request, 'painel_espetos.html', {'espetos': todos_espetos})

@staff_member_required
def deletar_espeto(request, id):
    espeto = Espeto.objects.get(id=id) # id = id especifica a coluna do BD
    espeto.delete()
    return redirect('painel_espetos')

@staff_member_required
def editar_espeto(request, id):
    espeto = Espeto.objects.get(id=id)

    if request.method == 'POST':
        # 1. Pegar os novos dados enviados pelo formulário
        # 2. Atualizar os atributos do espeto
        # 3. Salvar no banco com espeto.save()
        # 4. Redirecionar para o painel
        novo_nome = request.POST.get('nome')
        novo_tipo = request.POST.get('tipo')
        novo_preco = request.POST.get('preco')
        novo_preco = novo_preco.replace(',', '.')
        espeto.nome = novo_nome
        espeto.tipo = novo_tipo
        espeto.preco = novo_preco
        espeto.save()
        return redirect('painel_espetos')
    else:
        # Quando for GET: carregar a página/formulário com os dados do espeto
        return render(request, 'editar_espeto.html', {'espeto': espeto})
        
@staff_member_required
def adicionar_espeto(request):
    espeto = Espeto()

    if request.method == 'POST':
        novo_nome = request.POST.get('nome')
        novo_tipo = request.POST.get('tipo')
        novo_preco = request.POST.get('preco')
        novo_preco = novo_preco.replace(',', '.')
        espeto.nome = novo_nome
        espeto.tipo = novo_tipo
        espeto.preco = novo_preco
        espeto.save()
        return redirect('painel_espetos')
    else:
        # Quando for GET: carregar a página/formulário com os dados do espeto
        return render(request, 'adicionar_espeto.html', {'espeto': espeto})
