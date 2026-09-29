# Fluxo Básico de Versionamento (Git + GitHub)

Este documento descreve os passos exatos utilizados para preparar o repositório local, vincular a conta via token de segurança e enviar o código para a nuvem.

## 1. Inicialização e Preparação
Dentro do terminal (usando WSL), na pasta raiz do projeto:
* `git init`: Inicia o repositório local do Git.
* `git add .`: Prepara e adiciona todos os arquivos permitidos ao palco do Git (ignorando o que está listado no `.gitignore`).

## 2. Salvando o Estado (Commit)
Criamos um pacote com as alterações feitas.
* `git commit -m "Mensagem descrevendo as atualizações"`

## 3. Configuração de Identidade 
* `git config --global user.email "E-mail"`
* `git config --global user.name "Nome"`

## 4. Vinculando ao GitHub e Enviando (Push)
Vinculamos a pasta local ao repositório vazio criado na web:
* `git remote add origin https://github.com/seu-usuario/espetaria-django.git`
* `git branch -M main`

## 5. Futuros Commits (O fluxo do dia a dia)
Uma vez que o repositório já está criado e conectado, `init`, `remote add` ou `branch` são desnecessários. Toda vez que você alterar, apagar ou criar novos códigos, o ciclo será apenas este:

1. **Verificar o estado (Opcional, mas recomendado):**
   * `git status`: Mostra em vermelho o que foi alterado e em verde o que já está pronto para ser salvo.
2. **Preparar os arquivos:**
   * `git add .`: Adiciona todas as modificações de uma vez.
   * *(Opcional)* `git add nome_do_arquivo.py`: Adiciona apenas um arquivo específico.
3. **Empacotar a alteração:**
   * `git commit -m "Adiciona funcionalidade X na tela Y"`
4. **Subir para a nuvem:**
   * `git push`: Como o repositório já conhece o caminho, basta digitar isso para enviar ao GitHub (cole seu Token se o terminal pedir).

**IMPORTANTE**: `git pull` puxa as novidades da nuvem e deixa o PC atualizado.