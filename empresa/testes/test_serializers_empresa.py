import pytest
from datetime import date
from rest_framework.exceptions import ValidationError as DRFValidationError
from empresa.serializers import EmpresaSerializer
from empresa.models import Empresa


class TestEmpresaSerializer:

    def test_serializer_valido(self, db):
        data = {
            "nome": "Empresa Teste LTDA",
            "cnpj": "12345678901234",
            "endereco": "Rua Teste, 123",
            "data_fundacao": "2020-01-01"
        }
        
        serializer = EmpresaSerializer(data=data)
        assert serializer.is_valid()
        
        empresa = serializer.save()
        assert empresa.nome == "Empresa Teste LTDA"
        assert empresa.cnpj == "12345678901234"
        assert empresa.endereco == "Rua Teste, 123"
        assert empresa.data_fundacao == date(2020, 1, 1)

    def test_serializer_deserializacao(self, empresa_sample):
        serializer = EmpresaSerializer(empresa_sample)
        data = serializer.data
        
        assert data["nome"] == empresa_sample.nome
        assert data["cnpj"] == empresa_sample.cnpj
        assert data["endereco"] == empresa_sample.endereco
        assert data["data_fundacao"] == empresa_sample.data_fundacao.isoformat()

    def test_serializer_update(self, empresa_sample):
        data = {
            "nome": "Empresa Atualizada LTDA",
            "cnpj": empresa_sample.cnpj,
            "endereco": "Novo Endereço, 456",
            "data_fundacao": "2021-01-01"
        }
        
        serializer = EmpresaSerializer(empresa_sample, data=data)
        assert serializer.is_valid()
        
        empresa = serializer.save()
        assert empresa.nome == "Empresa Atualizada LTDA"
        assert empresa.endereco == "Novo Endereço, 456"

    def test_serializer_campos_obrigatorios(self, db):
        serializer = EmpresaSerializer(data={})
        assert not serializer.is_valid()
        assert "nome" in serializer.errors
        assert "cnpj" in serializer.errors
        assert "endereco" in serializer.errors
        assert "data_fundacao" in serializer.errors

    def test_serializer_cnpj_duplicado(self, db, empresa_sample):
        data = {
            "nome": "Outra Empresa",
            "cnpj": empresa_sample.cnpj,
            "endereco": "Outro Endereço",
            "data_fundacao": "2020-01-01"
        }
        
        serializer = EmpresaSerializer(data=data)
        assert not serializer.is_valid()
        assert "cnpj" in serializer.errors

