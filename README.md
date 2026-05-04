# Burguer App - Microservicos em Flask com uv Workspace

Projeto de estudo com arquitetura de microservicos para uma aplicacao de hamburgueria.
Cada dominio roda em um servico Flask separado, com banco MongoDB compartilhado,
e o gerenciamento de ambiente/dependencias e feito com uv workspace.

## Visao geral

O sistema e dividido em quatro servicos:

- auth-service: autenticacao, login, dashboard e controle de sessao.
- user-service: cadastro, consulta, edicao e exclusao de usuarios.
- product-service: catalogo de produtos, administracao e APIs de produtos/categorias.
- order-service: criacao, listagem, detalhes, atualizacao de status e exclusao de pedidos.

Todos os servicos usam o banco burguer_app_db no MongoDB.

## Arquitetura

Cada servico segue organizacao em camadas:

- config: conexao com banco.
- models: serializacao e formato dos dados.
- services: regras de negocio.
- controllers: rotas Flask e integracao com templates.
- templates/static: interface web.

## Fluxo funcional

1. O usuario acessa o auth-service e faz login.
2. Se nao tiver cadastro, auth-service redireciona para user-service.
3. user-service salva o usuario com senha hash.
4. auth-service valida credenciais, cria token JWT e salva dados em sessao.
5. order-service cria pedidos e pode consultar produtos do product-service por API.
6. product-service oferece listagem/catalogo e endpoints JSON para integracao.

## Workspace com uv

O repositorio usa uv workspace na raiz para agrupar os quatro servicos:

- burguer-app/auth-service
- burguer-app/order-service
- burguer-app/product-service
- burguer-app/user-service

Com isso, voce mantem:

- um unico ambiente virtual na raiz (.venv)
- um unico lockfile (uv.lock)
- pyproject.toml proprio em cada servico

## Pre-requisitos

- Python 3.13+
- uv instalado
- Docker Desktop (ou Docker Engine + Compose)

Instalacao do uv (Windows PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

## Configuracao de ambiente

Defina as variaveis de ambiente necessarias antes de subir os servicos.
Voce pode usar um arquivo .env na raiz do projeto.

Use o arquivo .env.example como base:

```bash
cp .env.example .env
```

Exemplo de .env:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=burguer_app_db
SECRET_KEY=troque-por-uma-chave-segura
```

Observacao:

- auth-service usa SECRET_KEY para sessao Flask.
- todos os servicos usam MONGO_URI para conectar no MongoDB.
- MONGO_DB_NAME permite trocar o nome do banco sem alterar codigo.

## Subir MongoDB local com Docker

Na raiz do projeto:

```bash
docker compose up -d mongodb
```

Verificar se o container esta saudavel:

```bash
docker compose ps
```

Parar o MongoDB:

```bash
docker compose stop mongodb
```

Parar e remover com volume (limpa dados locais):

```bash
docker compose down -v
```

## Como rodar local com uv

1. Suba o MongoDB com Docker.
2. Na raiz do projeto, sincronize o workspace:

```bash
uv sync
```

3. Suba cada servico em um terminal separado.

### Terminal 1 - auth-service (porta 5000)

```bash
uv run --package auth-service python burguer-app/auth-service/app.py
```

### Terminal 2 - user-service (porta 5001)

```bash
uv run --package user-service python burguer-app/user-service/app.py
```

### Terminal 3 - order-service (porta 5002)

```bash
uv run --package order-service python burguer-app/order-service/app.py
```

### Terminal 4 - product-service (porta 5003)

```bash
uv run --package product-service python burguer-app/product-service/app.py
```

## URLs locais

- Auth: http://localhost:5000
- User: http://localhost:5001
- Order: http://localhost:5002
- Product: http://localhost:5003

Endpoints de integracao importantes:

- GET http://localhost:5003/product/api/products
- GET http://localhost:5003/product/api/categories

## Testes

Atualmente, a suite de testes principal esta no auth-service.

Executar testes do auth-service:

```bash
uv run --package auth-service pytest -v
```

Executar com cobertura:

```bash
uv run --package auth-service pytest --cov=models --cov=controllers --cov=services --cov=config --cov-report=term-missing
```

Observacao sobre banco em testes:

- auth-service possui fallback para mongomock em ambiente de teste
- isso reduz dependencia de MongoDB real durante a execucao dos testes

## Qualidade de codigo

Para analise estatica com pylint no auth-service:

```bash
uv run --package auth-service pylint burguer-app/auth-service/config
uv run --package auth-service pylint burguer-app/auth-service/controllers
```

## Estrutura resumida

```text
python_pytest/
|-- pyproject.toml
|-- uv.lock
|-- burguer-app/
|   |-- auth-service/
|   |-- order-service/
|   |-- product-service/
|   |-- user-service/
```

## Problemas comuns

1. Erro de conexao com MongoDB
	- Verifique se o container mongodb esta em execucao com docker compose ps.
	- Verifique se MONGO_URI e MONGO_DB_NAME no .env estao corretos.

2. Falha ao abrir rotas entre servicos
	- Confirme se os quatro servicos estao rodando nas portas esperadas.

3. Dependencia faltando
	- Rode uv sync novamente na raiz.

## Melhorias futuras

- Adicionar testes para user-service, product-service e order-service.
- Padronizar lint/format para todos os servicos.
- Adicionar API gateway e observabilidade.