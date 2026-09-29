# Diário de Bordo: Preparando a Espetaria para o Mundo Real (Produção)

Esse é o meu guia pessoal de tudo o que rolou para tirar o projeto do ambiente local e preparar para a nuvem. A ideia aqui é entender o *porquê* de cada passo, lembrando dos perrengues e das soluções que usamos no WSL e no Supabase.

## 1. O Cofre de Segurança (.env e .gitignore)
A primeira regra que aprendi sobre colocar um site no ar: **nunca suba senhas para o GitHub**. 
* Criamos o arquivo `.gitignore` logo de cara. Ele é a "capa de invisibilidade" do Git. Tudo o que eu escrevo lá dentro, o Git ignora na hora de mandar pra nuvem.
* Colocamos pastas nativas do Python lá (`__pycache__`, `venv`, `miniconda3`) e, o mais importante, o arquivo `.env`.
* **O que é o `.env`?** É o nosso cofre. Criamos esse arquivo para guardar a `SECRET_KEY` (a senha mestra do Django) e, mais tarde, o link do banco de dados. 
* **O quase-acidente:** Em um momento, eu quase coloquei o meu token do GitHub escrito direto dentro do `.gitignore`. Se eu fizesse isso, o token subiria para a internet, porque o `.gitignore` em si é um arquivo público! Se eu quiser anotar o token pra não esquecer, o lugar certo é dentro do `.env` (que está protegido).

## 2. Ensinando o Django a ler o Cofre
Para o código Python conseguir enxergar o que estava dentro do arquivo `.env` sem expor os dados, instalamos duas ferramentas via `pip`:
* `python-dotenv`: Lê os textos do `.env`.
* `dj-database-url`: Converte o link do banco de dados em um formato que o Django aceita.
Lá no `settings.py`, apagamos as senhas fixas e colocamos o `os.environ.get('SECRET_KEY')`. Assim, o código puxa a chave dinamicamente.

## 3. A Saga do Banco de Dados (Supabase)
Meu código já estava usando PostgreSQL localmente, mas para o projeto virar produção de verdade, precisávamos de um banco na nuvem.
* Fui no Supabase. Tive um errinho de permissão inicial porque tentei criar o projeto na organização da empresa (onde eu não era admin). A solução foi criar a minha própria "Organization" gratuita e depois o projeto "espetaria-db".
* **O Bug do WSL (Network is unreachable):** Peguei a *Connection String* padrão do Supabase (porta 5432) e colei no `.env`. Quando rodei o `migrate`, o terminal explodiu um erro de rede. O motivo? O WSL do Windows se embanana todo com rotas IPv6 (que é o padrão novo do Supabase).
* **A Solução Mágica:** Voltei no Supabase, mudei a configuração para o **Connection Pooler** (que usa a porta 6543 e força o tráfego via IPv4). Colei o link novo no `.env` e o `migrate` rodou liso!
* **Bônus:** Como o banco do Supabase nasceu vazio, aquele erro chato que tínhamos antes (da "Mesa 34" que travava a Chave Estrangeira do pedido) simplesmente sumiu, porque as tabelas foram criadas do zero da forma certa.

## 4. O Rito de Passagem do Git e GitHub
Com o código blindado e o banco na nuvem, era hora de salvar o estado de tudo e mandar pro GitHub.
* Dei `git add .` e `git commit`. 
* Como era a primeira vez rodando isso no WSL, o terminal não sabia quem eu era e barrou o commit. Tive que rodar os comandos `git config --global user.email` e `user.name` com meus dados para assinar o pacote.
* **O Envio (Push):** Criei um repositório vazio no GitHub e vinculei no terminal (`git remote add origin...`). Quando fui dar o `git push`, o GitHub recusou a minha senha normal do site.
* **O Token de Acesso:** Descobri que o GitHub exige um "Personal Access Token" (PAT) para o terminal. Fui nas configurações de desenvolvedor do site, criei um token *Fine-grained* liberando acesso de "Read and write" em "Contents".
* **Pegadinha do Linux:** Na hora de colar esse token longo lá no WSL, a tela não mostrava nada (nem asteriscos), parecia que não tava digitando. É só colar "cego" e dar Enter. Funcionou, carregou 100%, e o código subiu seguro pro repositório!