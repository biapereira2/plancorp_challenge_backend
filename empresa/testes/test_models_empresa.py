import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date
from empresa.models import Empresa


class TestEmpresaModel:
    def test_criar_empresa(self, db):
        empresa = Empresa.objects.create(
            nome="Empresa Teste LTDA",
            cnpj="12345678901234",
            endereco="Rua Teste, 123",
            data_fundacao=date(2020, 1, 1)
        )
        
        assert empresa.id is not None
        assert empresa.nome == "Empresa Teste LTDA"
        assert empresa.cnpj == "12345678901234"
        assert empresa.endereco == "Rua Teste, 123"
        assert empresa.data_fundacao == date(2020, 1, 1)

    def test_empresa_str(self, db):
        empresa = Empresa.objects.create(
            nome="Empresa Teste LTDA",
            cnpj="12345678901234",
            endereco="Rua Teste, 123",
            data_fundacao=date(2020, 1, 1)
        )
        
        assert str(empresa) == "Empresa Teste LTDA"

    def test_cnpj_unico(self, db):
        Empresa.objects.create(
            nome="Empresa 1",
            cnpj="12345678901234",
            endereco="Endereço 1",
            data_fundacao=date(2020, 1, 1)
        )
        
        with pytest.raises(IntegrityError):
            Empresa.objects.create(
                nome="Empresa 2",
                cnpj="12345678901234",
                endereco="Endereço 2",
                data_fundacao=date(2020, 1, 1)
            )

    def test_cnpj_min_length(self, db):
        empresa = Empresa(
            nome="Empresa Teste",
            cnpj="1234567890",
            endereco="Endereço Teste",
            data_fundacao=date(2020, 1, 1)
        )
        
        with pytest.raises(ValidationError):
            empresa.full_clean()

    def test_campos_obrigatorios(self, db):
        empresa = Empresa()
        
        with pytest.raises(ValidationError):
            empresa.full_clean()

    def test_nome_max_length(self, db):
        empresa = Empresa(
            nome="A" * 101,
            cnpj="12345678901234",
            endereco="Endereço Teste",
            data_fundacao=date(2020, 1, 1)
        )
        
        with pytest.raises(ValidationError):
            empresa.full_clean()

    def test_endereco_max_length(self, db):
        empresa = Empresa(
            nome="Empresa Teste",
            cnpj="12345678901234",
            endereco="A" * 256,
            data_fundacao=date(2020, 1, 1)
        )
        
        with pytest.raises(ValidationError):
            empresa.full_clean()
