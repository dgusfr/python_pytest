# Guia Completo de Testes em Python com Pytest e Unittest

**Documento de Referência para Implementação de Testes Unitários, de Integração e de Cobertura**

---

## Índice
1. [Fundamentação Teórica](#fundamentação-teórica)
2. [Pytest - Framework Principal](#pytest---framework-principal)
3. [Cobertura de Testes](#cobertura-de-testes)
4. [Configuração Centralizada](#configuração-centralizada)
5. [Análise Estática com Pylint](#análise-estática-com-pylint)
6. [Mocks e Simulações](#mocks-e-simulações)
7. [Testes Parametrizados](#testes-parametrizados)
8. [Fixtures e conftest.py](#fixtures-e-conftestpy)
9. [Testes de Integração](#testes-de-integração)

---

## Fundamentação Teórica

### O que é Teste de Software?

Testes de software são processos sistemáticos para validar se uma aplicação funciona conforme o esperado. Seu objetivo primário é:

- **Detectar erros** antes que afetem o usuário final
- **Garantir qualidade** e confiabilidade do código
- **Assegurar experiência do usuário** adequada
- **Reduzir custos** e riscos de falhas em produção

### Tipos de Testes

#### 1. **Teste Unitário**
- Verifica unidades isoladas do código (funções, métodos, classes)
- Foco: lógica individual
- Escopo: pequeno e bem delimitado
- Velocidade: muito rápido
- Frequência: executado a cada mudança de código

#### 2. **Teste de Integração**
- Avalia a interação entre dois ou mais módulos
- Foco: comunicação entre componentes
- Escopo: médio
- Velocidade: mais lento que testes unitários
- Frequência: executado em etapas específicas do desenvolvimento

#### 3. **Teste de Regressão**
- Garante que novas alterações não introduzam bugs em funcionalidades existentes
- Foco: funcionalidades já implementadas
- Escopo: amplo
- Velocidade: varia
- Frequência: antes de cada deploy

#### 4. **Teste de Aceitação**
- Validação final pelo usuário
- Foco: requisitos funcionais
- Escopo: todo o sistema
- Velocidade: mais lento
- Frequência: antes de release para produção

---

## Pytest - Framework Principal

### O que é Pytest?

Pytest é um framework de testes em Python que:
- Suporta testes unitários, integração e parametrização
- Facilita criação de mocks e fixtures
- Oferece plugins para cobertura de teste
- Segue metodologias TDD (Test-Driven Development)
- Automatiza testes de regressão

### Instalação

```bash
# Instalação básica
pip install pytest

# Com todas as dependências do projeto
pip install -r requirements.txt
```

### Estrutura Básica de um Teste

```python
import pytest
from seu_modulo import funcao_a_testar

def test_funcao_simples():
    """
    Testa um comportamento específico da função.
    
    Convenção: nomes de funções de teste começam com 'test_'
    """
    # Setup: Preparar dados de entrada
    entrada = "valor_esperado"
    
    # Action: Executar a função
    resultado = funcao_a_testar(entrada)
    
    # Assert: Verificar o resultado
    assert resultado == "valor_esperado"
```

### Padrão AAA (Arrange, Act, Assert)

Todos os testes devem seguir este padrão:

| Etapa | Descrição | Exemplo |
|-------|-----------|---------|
| **Arrange** | Preparar dados e ambiente | `user = {"email": "teste@teste.com"}` |
| **Act** | Executar a função testada | `resultado = serialize_user(user)` |
| **Assert** | Validar resultado | `assert resultado == esperado` |

### Exemplo Prático: Teste de Serviço de Autenticação

```python
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from models.user_model import serialize_user

def test_serialize_user_completo():
    """
    Testa a serialização de um usuário com todos os campos preenchidos.
    
    Objetivo: Validar que a função retorna um dicionário com os dados corretos.
    """
    # Arrange
    user = {
        "email": "teste@exemplo.com",
        "name": "Teste Usuário",
        "address": "123 Rua Exemplo",
        "role": "admin"
    }
    
    # Act
    resultado = serialize_user(user)
    
    # Assert
    esperado = {
        "email": "teste@exemplo.com",
        "name": "Teste Usuário",
        "address": "123 Rua Exemplo",
        "role": "admin"
    }
    assert resultado == esperado
```

### Executando Testes

```bash
# Executar todos os testes no projeto
pytest

# Executar arquivo específico
pytest test_user_model.py

# Executar função de teste específica
pytest test_user_model.py::test_serialize_user_completo

# Modo verbose (mostra detalhes)
pytest -v

# Parar no primeiro erro
pytest -x

# Mostrar prints durante execução
pytest -s
```

---

## Cobertura de Testes

### O que é Cobertura de Testes?

Cobertura de testes é uma métrica que avalia a proporção do código-fonte executada durante os testes automatizados. Ela ajuda a:

- Identificar código não testado
- Garantir qualidade do código
- Detectar lógicas não cobertas
- Melhorar a confiabilidade da aplicação

**Ferramenta**: pytest-cov (plugin do pytest)

### Instalação do pytest-cov

```bash
pip install pytest-cov
```

### Executando Testes com Cobertura

```bash
# Execução básica com cobertura
pytest --cov=models.user_model

# Cobertura em múltiplos módulos
pytest --cov=models --cov=controllers --cov=services

# Gerar relatório em terminal (mostra linhas não cobertas)
pytest --cov=models --cov-report=term-missing

# Gerar relatório HTML (abre em navegador)
pytest --cov=models --cov-report=html

# Falhar se cobertura for menor que 80%
pytest --cov=models --cov-fail-under=80

# Combinação completa
pytest --cov=models --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

### Exemplo Prático: Teste com Cobertura

```python
import pytest
from models.user_model import User

class User:
    """Modelo de usuário para teste."""
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def serialize_user(self):
        """Converte usuário para dicionário."""
        return {
            'username': self.username,
            'email': self.email
        }

# Teste
def test_serialize_user():
    """Testa serialização do usuário."""
    # Arrange
    user = User("testuser", "test@example.com")
    
    # Act
    serialized_data = user.serialize_user()
    
    # Assert
    assert isinstance(serialized_data, dict)
    assert serialized_data['username'] == "testuser"
    assert serialized_data['email'] == "test@example.com"
```

### Interpretando Resultados de Cobertura

```
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
models/user.py       10      2    80%    15-16
models/order.py       8      0   100%
-----------------------------------------------
TOTAL               18      2    89%
```

- **Stmts**: Número total de linhas de código
- **Miss**: Linhas não executadas nos testes
- **Cover**: Percentual de cobertura
- **Missing**: Números das linhas não cobertas

---

## Configuração Centralizada

### Arquivo pytest.ini

O arquivo `pytest.ini` centraliza todas as configurações do pytest, evitando repetição de comandos e melhorando a produtividade.

**Localização**: Raiz do projeto

### Benefícios

- Evita repetir flags de linha de comando
- Mantém consistência entre testes
- Facilita integração em CI/CD
- Documenta padrões do projeto

### Exemplo de pytest.ini

```ini
[pytest]
# Diretórios onde os testes estão localizados
testpaths = test

# Padrão de nomes de arquivos de teste
python_files = test_*.py

# Padrão de nomes de funções de teste
python_functions = test_*

# Padrão de nomes de classes de teste
python_classes = Test*

# Opciones de execução padrão
addopts = -v --cov=models --cov=controllers --cov=services --cov=config --cov-report=term-missing --cov-fail-under=80

# Variáveis de ambiente
markers =
    slow: marca teste como lento
    integration: marca teste como integração
    unit: marca teste como unitário
```

### Usando Configurações do pytest.ini

Uma vez definido o arquivo, execute simplesmente:

```bash
# Usa todas as configurações definidas em pytest.ini
pytest

# Ainda é possível sobrescrever opções específicas
pytest -v --cov-fail-under=90
```

### Estrutura Recomendada do Projeto

```
seu_projeto/
├── models/
│   ├── __init__.py
│   └── user_model.py
├── controllers/
│   ├── __init__.py
│   └── user_controller.py
├── services/
│   ├── __init__.py
│   └── user_service.py
├── config/
│   ├── __init__.py
│   └── database.py
├── test/
│   ├── test_user_model.py
│   ├── test_user_controller.py
│   └── test_user_service.py
├── pytest.ini          # Configuração centralizada
├── pyproject.toml      # Configurações do projeto
└── requirements.txt    # Dependências
```

---

## Análise Estática com Pylint

### O que é Pylint?

Pylint é uma ferramenta de análise estática que:
- Baseia-se no guia de estilos PEP 8
- Examina código-fonte em busca de erros
- Detecta bugs e problemas de estilo
- Melhora qualidade e legibilidade
- Integra-se em pipelines CI/CD

### Instalação

```bash
pip install pylint
```

### Uso Básico

```bash
# Analisar um arquivo
pylint seu_arquivo.py

# Analisar um diretório
pylint seu_projeto/

# Gerar relatório em formato específico
pylint --output-format=json seu_arquivo.py > report.json

# Usar apenas regras específicas
pylint --disable=missing-docstring seu_arquivo.py
```

### Tipos de Mensagens Pylint

| Tipo | Código | Descrição | Exemplo |
|------|--------|-----------|---------|
| **Convention** | C | Problemas de estilo | C0301: Linha muito longa |
| **Refactor** | R | Sugestões de melhoria | R0914: Muitas variáveis locais |
| **Warning** | W | Possíveis problemas | W0612: Variável não usada |
| **Error** | E | Erros de sintaxe | E0601: Usado antes da atribuição |
| **Fatal** | F | Erro fatal | F0401: Importação não encontrada |

### Exemplo Prático

**Código Original (Com Problemas)**:
```python
def soma(a, b):
    resultado = a + b
    return resultado

x = 10
y = 5
print(soma(x, y))
```

**Análise do Pylint**:
```
C0301: Line too long (82/80): Linha excede o limite de 80 caracteres
C0114: Missing module docstring: Falta docstring do módulo
C0103: Invalid name for x (should match [a-z_][a-z0-9_]*): Nome inadequado
```

**Código Corrigido**:
```python
"""Módulo com funções matemáticas básicas."""


def soma(num1, num2):
    """
    Soma dois números.
    
    Args:
        num1: Primeiro número
        num2: Segundo número
        
    Returns:
        int: Resultado da soma
    """
    resultado = num1 + num2
    return resultado


# Exemplo de uso
primeiro_numero = 10
segundo_numero = 5
print(soma(primeiro_numero, segundo_numero))
```

### Configuração do Pylint

Crie `.pylintrc` na raiz do projeto:

```ini
[MASTER]
load-plugins=pylint_django

[MESSAGES CONTROL]
disable=missing-docstring,too-few-public-methods

[FORMAT]
max-line-length=100

[DESIGN]
max-attributes=7
max-arguments=5
```

---

## Mocks e Simulações

### O que é Mock?

Mock é uma simulação de um objeto ou função que:
- Isola o código testado de dependências externas
- Fornece comportamento predefinido
- Permite validar chamadas e parâmetros
- Torna testes mais rápidos e determinísticos

### Quando Usar Mocks?

| Cenário | Motivo | Exemplo |
|---------|--------|---------|
| **Banco de dados** | Evitar conexões reais | Simular MongoDB |
| **APIs externas** | Evitar chamadas reais | Simular resposta HTTP |
| **Sistema de arquivos** | Não modificar arquivos | Simular leitura/escrita |
| **Serviços de email** | Não enviar emails reais | Simular envio |
| **Chamadas HTTP** | Não depender de conexão | Simular resposta de servidor |

### Ferramentas

- **unittest.mock**: Incluído na stdlib Python
- **patch**: Decorator/context manager
- **MagicMock**: Classe para objetos mock dinâmicos

### Exemplo 1: Simular Conexão com Banco de Dados

```python
import unittest
from unittest.mock import patch, MagicMock

# Código a ser testado
def conectar_ao_banco():
    """Simula conexão com banco de dados."""
    print("Conectando ao banco de dados...")
    return "Conexão estabelecida"

def executar_query(conexao, query):
    """Executa query no banco de dados."""
    print(f"Executando query: {query}")
    return "Resultado da query"

def funcao_que_usa_o_banco(query):
    """Função que depende do banco de dados."""
    conexao = conectar_ao_banco()
    resultado = executar_query(conexao, query)
    return resultado

# Teste com mock
class TestFuncaoQueUsaOBanco(unittest.TestCase):
    """Testes para função que usa banco de dados."""
    
    @patch('__main__.conectar_ao_banco')
    @patch('__main__.executar_query')
    def test_funcao_que_usa_o_banco(self, mock_executar_query, mock_conectar_ao_banco):
        """
        Testa função usando mocks para dependências externas.
        
        Nota: Decoradores aplicados de baixo para cima, então parâmetros
        estão em ordem inversa.
        """
        # Arrange: Configurar mocks
        mock_conectar_ao_banco.return_value = "Conexão mockada"
        mock_executar_query.return_value = "Resultado mockado"

        # Act: Executar função
        resultado = funcao_que_usa_o_banco("SELECT * FROM tabela")

        # Assert: Validar resultado e chamadas
        assert resultado == "Resultado mockado"
        mock_conectar_ao_banco.assert_called_once()
        mock_executar_query.assert_called_once_with(
            "Conexão mockada", 
            "SELECT * FROM tabela"
        )
```

### Exemplo 2: Simular MongoDB

```python
import os
import sys
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import get_db

def test_get_db():
    """
    Testa função get_db sem conectar ao MongoDB real.
    
    Objetivo: Simular a conexão sem depender da disponibilidade do banco.
    """
    # Arrange: Simular MongoClient
    with patch('pymongo.MongoClient') as mock_client:
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db

        # Act: Aplicar mock e executar função
        with patch("config.database.client", mock_client):
            db_instance = get_db()

            # Assert: Validar resultado
            assert db_instance == mock_db
            assert db_instance is not None
```

### Métodos de Validação de Mocks

```python
from unittest.mock import Mock, call

mock = Mock()
mock.metodo(1, 2, 3)
mock.metodo(4, 5, 6)

# Validar se foi chamado
mock.metodo.assert_called()

# Validar chamada específica
mock.metodo.assert_called_with(4, 5, 6)

# Validar número de chamadas
assert mock.metodo.call_count == 2

# Validar todas as chamadas
assert mock.metodo.call_args_list == [call(1, 2, 3), call(4, 5, 6)]

# Validar chamada única
mock.metodo.assert_called_once()
```

---

## Testes Parametrizados

### O que é Parametrização?

Parametrização permite executar um mesmo teste múltiplas vezes com diferentes conjuntos de dados, eliminando duplicação de código.

### Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Reduz duplicação** | Um teste, múltiplos casos |
| **Melhora legibilidade** | Casos claros em lista |
| **Facilita manutenção** | Adicionar casos é trivial |
| **Aumenta cobertura** | Mais cenários testados |

### Sintaxe Básica

```python
import pytest

@pytest.mark.parametrize("parametro1, parametro2, esperado", [
    (valor1, valor2, resultado1),
    (valor3, valor4, resultado2),
    (valor5, valor6, resultado3)
])
def test_funcao(parametro1, parametro2, esperado):
    resultado = funcao(parametro1, parametro2)
    assert resultado == esperado
```

### Exemplo 1: Teste de Soma

```python
import pytest

def somar(a, b):
    """Soma dois números."""
    return a + b

@pytest.mark.parametrize("num1, num2, esperado", [
    (1, 2, 3),              # Inteiros positivos
    (-1, 2, 1),             # Inteiro negativo
    (0, 0, 0),              # Zeros
    (2.5, 2.5, 5.0),        # Ponto flutuante
    (-5, -3, -8),           # Inteiros negativos
])
def test_somar(num1, num2, esperado):
    """Testa adição com múltiplos cenários."""
    assert somar(num1, num2) == esperado
```

### Exemplo 2: Teste de API com Diferentes Tipos

**Antes (Sem Parametrização)**:
```python
def test_api_inteiro():
    resposta = api_call(10)
    assert resposta == "Inteiro"

def test_api_string():
    resposta = api_call("texto")
    assert resposta == "String"

def test_api_booleano():
    resposta = api_call(True)
    assert resposta == "Booleano"
```

**Depois (Com Parametrização)**:
```python
import pytest

@pytest.mark.parametrize(
    "entrada, saida_esperada",
    [
        (10, "Inteiro"),
        ("texto", "String"),
        (True, "Booleano"),
        (3.14, "Float"),
        ([], "Lista"),
    ]
)
def test_api_tipos(entrada, saida_esperada):
    """Testa API com diferentes tipos de entrada."""
    resposta = api_call(entrada)
    assert resposta == saida_esperada, f"Falha para entrada: {entrada}"
```

### Parametrização Múltipla

```python
import pytest

@pytest.mark.parametrize("username", ["admin", "user", "guest"])
@pytest.mark.parametrize("password", ["123456", "abc123"])
def test_login(username, password):
    """
    Testa login com múltiplas combinações.
    Resulta em 3 x 2 = 6 testes.
    """
    resultado = fazer_login(username, password)
    assert resultado is not None
```

### Usando IDs para Melhor Legibilidade

```python
@pytest.mark.parametrize(
    "entrada, esperado",
    [
        (0, "zero"),
        (1, "um"),
        (-1, "negativo"),
    ],
    ids=["zero", "um", "negativo"]
)
def test_numero(entrada, esperado):
    assert converter_numero(entrada) == esperado
```

**Saída**:
```
test_numero[zero] PASSED
test_numero[um] PASSED
test_numero[negativo] PASSED
```

---

## Fixtures e conftest.py

### O que são Fixtures?

Fixtures são funções reutilizáveis que:
- Preparam ambiente de teste (setup)
- Fornecem dados e configurações
- Limpam recursos após teste (teardown)
- Permitem isolar testes
- Evitam repetição de código

### Padrão Setup-Yield-Teardown

```python
import pytest

@pytest.fixture
def recurso_teste():
    """
    Fixture com setup e teardown.
    """
    # Setup: Preparar recurso
    recurso = criar_recurso()
    print("Setup executado")
    
    # Yield: Fornecer recurso ao teste
    yield recurso
    
    # Teardown: Limpar recurso
    limpar_recurso(recurso)
    print("Teardown executado")

def test_com_fixture(recurso_teste):
    """Teste que usa a fixture."""
    assert recurso_teste is not None
```

### Escopos de Fixtures

| Escopo | Duração | Uso Comum |
|--------|---------|----------|
| **function** | Por teste | Configurações simples |
| **class** | Por classe de testes | Dados de classe |
| **module** | Por módulo de teste | Inicialização pesada |
| **session** | Sessão completa | Conexão com BD |

### Exemplo 1: Fixture com Arquivo Temporário

```python
import pytest
import os

@pytest.fixture(scope="function")
def setup_ambiente():
    """Fixture para preparar ambiente de teste."""
    # Setup: Criar arquivo temporário
    with open("temp_file.txt", "w") as f:
        f.write("Dados de teste")
    
    # Yield: Fornecer nome do arquivo
    yield "temp_file.txt"
    
    # Teardown: Remover arquivo
    os.remove("temp_file.txt")

def test_uso_arquivo(setup_ambiente):
    """Teste que usa arquivo temporário."""
    nome_arquivo = setup_ambiente
    with open(nome_arquivo, "r") as f:
        conteudo = f.read()
    
    assert conteudo == "Dados de teste"
```

### Exemplo 2: Fixture com Banco de Dados

```python
import pytest
from sua_aplicacao import criar_usuario, Usuario

@pytest.fixture(scope="function")
def usuario_teste():
    """Fixture que cria um usuário de teste."""
    # Arrange: Criar usuário
    usuario = criar_usuario(
        email="teste@teste.com",
        nome="Teste User",
        role="user"
    )
    
    # Yield para uso no teste
    yield usuario
    
    # Cleanup: Deletar usuário
    usuario.delete()

def test_usuario_criado(usuario_teste):
    """Testa propriedades do usuário."""
    assert usuario_teste.email == "teste@teste.com"
    assert usuario_teste.nome == "Teste User"
    assert usuario_teste.role == "user"
```

### conftest.py - Configuração Global

O arquivo `conftest.py` centraliza fixtures e configurações compartilhadas entre múltiplos testes.

**Localização**: Raiz do diretório de testes

**Benefícios**:
- Compartilha fixtures entre arquivos
- Centraliza configurações
- Evita duplicação
- Melhora manutenibilidade

### Estrutura do Projeto com conftest.py

```
seu_projeto/
├── models/
│   └── user_model.py
├── services/
│   └── user_service.py
├── test/
│   ├── conftest.py          # Configurações globais
│   ├── test_user_model.py
│   ├── test_user_service.py
│   └── integration/
│       ├── conftest.py      # Configurações de integração
│       └── test_full_flow.py
└── pytest.ini
```

### Exemplo 1: conftest.py com MongoDB

```python
"""
conftest.py
Configurações globais de teste.
"""

import pytest
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def mongo_client():
    """
    Fixture para criar conexão com MongoDB (escopo: session).
    
    Executada uma vez por sessão de testes.
    """
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(uri)
    
    # Verificar conexão
    try:
        client.admin.command('ping')
    except Exception as e:
        pytest.skip(f"MongoDB não disponível: {e}")
    
    yield client
    client.close()

@pytest.fixture(scope="function")
def test_db(mongo_client):
    """
    Fixture para fornecer BD de teste limpo (escopo: function).
    
    Executada para cada função de teste.
    """
    db = mongo_client["burguer_app_test"]
    
    # Limpar coleções
    db["users"].delete_many({})
    db["orders"].delete_many({})
    db["products"].delete_many({})
    
    yield db
    
    # Cleanup
    mongo_client.drop_database("burguer_app_test")

@pytest.fixture(scope="function")
def usuario_padrao(test_db):
    """
    Fixture que cria usuário padrão para testes.
    
    Depende de test_db (fixture parametrizada).
    """
    usuario = {
        "email": "teste@teste.com",
        "name": "Usuário Teste",
        "password": "senha123",
        "role": "user"
    }
    
    resultado = test_db["users"].insert_one(usuario)
    usuario["_id"] = resultado.inserted_id
    
    yield usuario
    
    test_db["users"].delete_one({"_id": usuario["_id"]})

@pytest.fixture(scope="function")
def usuario_admin(test_db):
    """Fixture que cria admin para testes."""
    admin = {
        "email": "admin@teste.com",
        "name": "Admin Teste",
        "password": "admin123",
        "role": "admin"
    }
    
    resultado = test_db["users"].insert_one(admin)
    admin["_id"] = resultado.inserted_id
    
    yield admin
    
    test_db["users"].delete_one({"_id": admin["_id"]})
```

### Usando Fixtures em Testes

```python
"""test_user_service.py"""

from services.user_service import autenticar_usuario

def test_autenticacao_valida(test_db, usuario_padrao):
    """
    Testa autenticação com usuário válido.
    
    Fixtures injetadas:
    - test_db: Banco de dados limpo
    - usuario_padrao: Usuário pré-criado
    """
    # Act
    resultado = autenticar_usuario(
        test_db,
        usuario_padrao["email"],
        "senha123"
    )
    
    # Assert
    assert resultado is not None
    assert resultado["email"] == usuario_padrao["email"]

def test_autenticacao_invalida(test_db, usuario_padrao):
    """Testa autenticação com senha incorreta."""
    # Act
    resultado = autenticar_usuario(
        test_db,
        usuario_padrao["email"],
        "senha_errada"
    )
    
    # Assert
    assert resultado is None

def test_admin_pode_criar_usuarios(test_db, usuario_admin):
    """Testa se admin pode criar usuários."""
    from services.user_service import criar_usuario
    
    novo_usuario = {
        "email": "novo@teste.com",
        "name": "Novo Usuário",
        "password": "senha456",
        "role": "user"
    }
    
    resultado = criar_usuario(test_db, novo_usuario, usuario_admin)
    
    assert resultado is not None
    assert resultado["email"] == "novo@teste.com"
```

### Padrão de Dependency Injection com Fixtures

```python
@pytest.fixture
def servico_usuario(test_db):
    """Fixture que cria serviço com dependências injetadas."""
    from services.user_service import UserService
    return UserService(db=test_db)

def test_servico_usuario(servico_usuario):
    """Usa serviço pré-configurado."""
    usuario = servico_usuario.criar_usuario({
        "email": "novo@teste.com",
        "name": "Novo"
    })
    assert usuario is not None
```

---

## Testes de Integração

### O que é Teste de Integração?

Testes de integração verificam a interação entre diferentes módulos ou serviços:
- Validam fluxo de dados
- Testam comunicação entre componentes
- Garantem consistência do sistema
- Abrangem múltiplos módulos

**Diferença dos Testes Unitários**:

| Aspecto | Unitário | Integração |
|--------|----------|------------|
| **Escopo** | Função isolada | Múltiplos módulos |
| **Velocidade** | Muito rápido | Mais lento |
| **Dependências** | Nenhuma | Várias |
| **Frequência** | A cada mudança | Etapas específicas |

### Exemplo de Arquitetura: Microsserviços

```
┌──────────────────────┐
│  Serviço de Auth     │
├──────────────────────┤
│ - Autenticação       │
│ - Geração de JWT     │
└──────────────────────┘
           ↓
┌──────────────────────┐
│  Serviço de Pedidos  │
├──────────────────────┤
│ - Criar pedido       │
│ - Listar pedidos     │
└──────────────────────┘
           ↓
┌──────────────────────┐
│ Serviço de Produtos  │
├──────────────────────┤
│ - Listar produtos    │
│ - Atualizar preço    │
└──────────────────────┘
```

### Exemplo 1: Teste de Integração com Requests

```python
"""test_integration.py"""

import pytest
import requests

# URLs dos serviços (configurar conforme ambiente)
BASE_URL_AUTH = "http://localhost:5000"
BASE_URL_ORDERS = "http://localhost:5001"
BASE_URL_PRODUCTS = "http://localhost:5002"

@pytest.fixture
def token_autenticacao():
    """Fixture que obtém token de autenticação."""
    dados_login = {
        "email": "teste@teste.com",
        "password": "senha123"
    }
    
    resposta = requests.post(
        f"{BASE_URL_AUTH}/auth/login",
        json=dados_login
    )
    
    assert resposta.status_code == 200
    token = resposta.json()["token"]
    
    return token

def test_fluxo_completo_pedido(token_autenticacao):
    """
    Testa fluxo completo: autenticação → criar pedido → validar.
    
    Integra 3 serviços.
    """
    headers = {"Authorization": f"Bearer {token_autenticacao}"}
    
    # Step 1: Obter produtos
    resposta_produtos = requests.get(
        f"{BASE_URL_PRODUCTS}/products",
        headers=headers
    )
    assert resposta_produtos.status_code == 200
    produtos = resposta_produtos.json()
    assert len(produtos) > 0
    
    produto_id = produtos[0]["id"]
    
    # Step 2: Criar pedido
    dados_pedido = {
        "produto_id": produto_id,
        "quantidade": 2,
        "endereco_entrega": "Rua Principal, 123"
    }
    
    resposta_pedido = requests.post(
        f"{BASE_URL_ORDERS}/orders",
        json=dados_pedido,
        headers=headers
    )
    assert resposta_pedido.status_code == 201
    pedido = resposta_pedido.json()
    pedido_id = pedido["id"]
    
    # Step 3: Validar pedido criado
    resposta_validacao = requests.get(
        f"{BASE_URL_ORDERS}/orders/{pedido_id}",
        headers=headers
    )
    assert resposta_validacao.status_code == 200
    pedido_validado = resposta_validacao.json()
    
    # Assertions finais
    assert pedido_validado["status"] == "pendente"
    assert pedido_validado["quantidade"] == 2
    assert pedido_validado["produto_id"] == produto_id

@pytest.mark.parametrize("quantidade", [1, 5, 10, 100])
def test_criar_pedidos_diferentes_quantidades(token_autenticacao, quantidade):
    """
    Testa criação de pedidos com diferentes quantidades.
    
    Combina: parametrização + integração.
    """
    headers = {"Authorization": f"Bearer {token_autenticacao}"}
    
    dados_pedido = {
        "produto_id": "123",
        "quantidade": quantidade,
        "endereco_entrega": "Rua Test"
    }
    
    resposta = requests.post(
        f"{BASE_URL_ORDERS}/orders",
        json=dados_pedido,
        headers=headers
    )
    
    assert resposta.status_code == 201
    pedido = resposta.json()
    assert pedido["quantidade"] == quantidade
```

### Exemplo 2: Teste de Integração com Context Manager

```python
import pytest

@pytest.fixture
def dados_validos():
    """Fixture com dados de teste."""
    return {"usuario_id": 123, "produto_id": 456}

def test_integracao_servico_a_b(dados_validos):
    """
    Testa comunicação entre dois serviços.
    
    Serviço A processa dados → Serviço B valida.
    """
    # Setup
    URL_SERVICO_A = "http://localhost:5000/api/servico_a"
    URL_SERVICO_B = "http://localhost:5001/api/servico_b"
    
    # Step 1: Serviço A processa
    resposta_a = requests.post(
        f"{URL_SERVICO_A}/processar",
        json=dados_validos
    )
    assert resposta_a.status_code == 200
    dados_resposta_a = resposta_a.json()
    
    # Step 2: Serviço B valida resultado
    resposta_b = requests.post(
        f"{URL_SERVICO_B}/validar",
        json=dados_resposta_a
    )
    assert resposta_b.status_code == 200
    
    # Validar resultado
    resultado = resposta_b.json()
    assert resultado["status"] == "sucesso"
    assert resultado["mensagem"] == "Processamento integrado"
```

### Boas Práticas para Testes de Integração

1. **Isolamento**: Use banco de dados de teste
2. **Limpeza**: Limpe dados após cada teste
3. **Timeout**: Defina timeouts para chamadas HTTP
4. **Mocks**: Mock de serviços não disponíveis
5. **Documentação**: Documente o fluxo testado
6. **Dados**: Use dados mínimos necessários

### Marcando Testes de Integração

```python
"""pytest.ini"""
[pytest]
markers =
    integration: marca teste como integração
    unit: marca teste como unitário
    slow: marca teste como lento
```

```python
"""test_integration.py"""

import pytest

@pytest.mark.integration
def test_fluxo_pedidos():
    """Teste marcado como integração."""
    pass

# Executar só testes de integração
# pytest -m integration

# Executar tudo exceto integração
# pytest -m "not integration"
```

---

## Checklist de Implementação

Use este checklist para implementar testes em seu projeto:

### Preparação Inicial
- [ ] Instalar pytest: `pip install pytest`
- [ ] Instalar pytest-cov: `pip install pytest-cov`
- [ ] Instalar pylint: `pip install pylint`
- [ ] Criar diretório `test/` na raiz do projeto

### Configuração Centralizada
- [ ] Criar `pytest.ini` na raiz
- [ ] Configurar opções de cobertura mínima
- [ ] Adicionar marcadores (unit, integration, slow)

### Testes Unitários
- [ ] Criar arquivo `test_modulo.py` para cada módulo
- [ ] Implementar testes usando padrão AAA
- [ ] Alcançar mínimo 80% de cobertura
- [ ] Validar com pylint

### Fixtures
- [ ] Criar `conftest.py` no diretório de testes
- [ ] Implementar fixture de BD para testes
- [ ] Implementar fixtures de dados padrão
- [ ] Documentar escopos das fixtures

### Testes de Integração
- [ ] Criar arquivo `test_integration.py`
- [ ] Testar fluxo completo entre serviços
- [ ] Usar marcador `@pytest.mark.integration`
- [ ] Validar comunicação entre módulos

### Qualidade
- [ ] Executar: `pytest --cov=. --cov-report=html`
- [ ] Analisar com pylint: `pylint seu_modulo.py`
- [ ] Alcançar score > 8.0 no pylint
- [ ] Revisar e refatorar testes conforme necessário

---

## Comandos Essenciais

```bash
# INSTALAÇÃO
pip install pytest pytest-cov pylint

# EXECUÇÃO BÁSICA
pytest                                    # Todos os testes
pytest -v                                 # Modo verbose
pytest -x                                 # Para no primeiro erro
pytest -s                                 # Mostra print()

# TESTES ESPECÍFICOS
pytest test_user.py                       # Arquivo específico
pytest test_user.py::test_login           # Função específica
pytest -k "test_login"                    # Por padrão de nome

# COBERTURA
pytest --cov=.                            # Cobertura de tudo
pytest --cov=models --cov-report=html    # Relatório HTML
pytest --cov=. --cov-fail-under=80       # Falha se < 80%

# MARCADORES
pytest -m unit                            # Só testes unitários
pytest -m "not integration"               # Excluir integração

# ANÁLISE ESTÁTICA
pylint seu_modulo.py                      # Analisar arquivo
pylint seu_projeto/                       # Analisar diretório
```

---

## Referências Rápidas

### Asserts Úteis

```python
assert resultado == esperado              # Igualdade
assert resultado is not None              # Não nulo
assert len(lista) == 3                    # Tamanho
assert "texto" in resultado               # Contém
assert isinstance(obj, dict)              # Tipo
assert resultado > 0                      # Comparação
```

### Mocks Úteis

```python
from unittest.mock import patch, MagicMock

@patch('modulo.funcao')
def test_com_mock(mock_funcao):
    mock_funcao.return_value = "valor"
    mock_funcao.assert_called_once()

mock = MagicMock()
mock.metodo.return_value = "resultado"
```

### Fixtures Úteis

```python
@pytest.fixture(scope="function")
def recurso():
    # Setup
    yield valor
    # Teardown

def test_funcao(recurso):
    assert recurso is not None
```

---

## Conclusão

Este guia fornece uma base sólida para implementar testes de qualidade em projetos Python. Lembre-se:

1. **Sempre escrever testes** antes ou junto com o código
2. **Manter testes simples** e focados
3. **Usar padrão AAA** em todos os testes
4. **Automatizar execução** de testes
5. **Monitorar cobertura** constantemente
6. **Refatorar testes** conforme o código evolui

Bons testes = Código de qualidade = Menos bugs = Usuários felizes!

---

**Documento criado em**: Maio de 2026  
**Versão**: 1.0  
**Status**: Produção
