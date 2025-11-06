# Testes Unitários do Backend

Este projeto utiliza pytest e pytest-django para testes unitários.

## Instalação

1. Certifique-se de que o ambiente virtual está ativado:
```bash
# No Windows
.\env\Scripts\activate

# No Linux/Mac
source env/bin/activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando os Testes

### Executar todos os testes:
```bash
pytest
```

### Executar testes de um app específico:
```bash
pytest empresa/
pytest acionista/
```

### Executar testes com cobertura:
```bash
pytest --cov=empresa --cov=acionista --cov-report=html
```

### Executar testes com output detalhado:
```bash
pytest -v
```

### Executar testes específicos:
```bash
pytest empresa/tests.py::TestEmpresaModel::test_criar_empresa
```

## Estrutura dos Testes

Os testes estão organizados da seguinte forma:

- **`conftest.py`**: Fixtures compartilhadas (empresa_sample, acionista_sample, etc.)
- **`pytest.ini`**: Configuração do pytest
- **`empresa/tests.py`**: Testes para o modelo Empresa
- **`empresa/test_serializers.py`**: Testes para o EmpresaSerializer
- **`empresa/test_views.py`**: Testes para o EmpresaViewSet
- **`acionista/tests.py`**: Testes para os modelos Acionista e Participacao
- **`acionista/test_serializers.py`**: Testes para os serializers
- **`acionista/test_views.py`**: Testes para os viewsets

## Observações Importantes

⚠️ **Atenção**: Os métodos customizados no `ParticipacaoViewSet` estão nomeados como `criar`, `atualizar`, `deletar`, mas no Django REST Framework os métodos corretos são `create`, `update`, `destroy`. 

Para que os métodos customizados funcionem corretamente, você precisa renomeá-los:

- `criar()` → `create()`
- `atualizar()` → `update()`
- `deletar()` → `destroy()`

O mesmo se aplica aos métodos do `ParticipacaoSerializer`:
- `criar()` → `create()`
- `atualizar()` → `update()`

Além disso, o modelo `Empresa` não possui o campo `percentual_vendido` que está sendo referenciado nos métodos do serializer. Você pode precisar:
1. Adicionar esse campo ao modelo, ou
2. Remover essas referências do serializer

## Cobertura de Testes

Os testes cobrem:
- ✅ Criação, leitura, atualização e deleção de modelos
- ✅ Validações de campos obrigatórios
- ✅ Validações de unicidade (CPF, CNPJ, email)
- ✅ Validações de tamanho mínimo e máximo
- ✅ Relacionamentos entre modelos (cascade delete)
- ✅ Serialização e deserialização
- ✅ Endpoints da API (GET, POST, PUT, PATCH, DELETE)
- ✅ Validações de negócio (percentual total não exceder 100%)

