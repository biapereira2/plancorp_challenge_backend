import pytest
from django.contrib.auth.models import User
from datetime import date, datetime
from decimal import Decimal
from empresa.models import Empresa
from acionista.models import Acionista, Participacao


@pytest.fixture
def empresa_sample(db):
    return Empresa.objects.create(
        nome="Empresa Teste LTDA",
        cnpj="12345678901234",
        endereco="Rua Teste, 123",
        data_fundacao=date(2020, 1, 1)
    )


@pytest.fixture
def empresa_sample_2(db):
    return Empresa.objects.create(
        nome="Empresa Teste 2 LTDA",
        cnpj="98765432109876",
        endereco="Avenida Teste, 456",
        data_fundacao=date(2018, 5, 15)
    )


@pytest.fixture
def acionista_sample(db):
    return Acionista.objects.create(
        nome="João Silva",
        cpf="12345678901",
        email="joao@example.com"
    )


@pytest.fixture
def acionista_sample_2(db):
    return Acionista.objects.create(
        nome="Maria Santos",
        cpf="98765432109",
        email="maria@example.com"
    )


@pytest.fixture
def participacao_sample(db, empresa_sample, acionista_sample):
    return Participacao.objects.create(
        acionista=acionista_sample,
        empresa=empresa_sample,
        percentual=Decimal("25.50")
    )