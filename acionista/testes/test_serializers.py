import pytest
from decimal import Decimal
from rest_framework.exceptions import ValidationError as DRFValidationError

from acionista.serializers import AcionistaSerializer, ParticipacaoSerializer
from acionista.models import Acionista, Participacao
from empresa.models import Empresa


class TestAcionistaSerializer:
    def test_serializer_valido(self, db):
        data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "email": "joao@example.com"
        }
        
        serializer = AcionistaSerializer(data=data)
        assert serializer.is_valid()
        
        acionista = serializer.save()
        assert acionista.nome == "João Silva"
        assert acionista.cpf == "12345678901"
        assert acionista.email == "joao@example.com"

    def test_serializer_deserializacao(self, acionista_sample):
        serializer = AcionistaSerializer(acionista_sample)
        data = serializer.data
        
        assert data["nome"] == acionista_sample.nome
        assert data["cpf"] == acionista_sample.cpf
        assert data["email"] == acionista_sample.email

    def test_serializer_update(self, acionista_sample):
        data = {
            "nome": "João Silva Atualizado",
            "cpf": acionista_sample.cpf,
            "email": "joao.atualizado@example.com"
        }
        
        serializer = AcionistaSerializer(acionista_sample, data=data)
        assert serializer.is_valid()
        
        acionista = serializer.save()
        assert acionista.nome == "João Silva Atualizado"
        assert acionista.email == "joao.atualizado@example.com"

    def test_serializer_campos_obrigatorios(self, db):
        serializer = AcionistaSerializer(data={})
        assert not serializer.is_valid()
        assert "nome" in serializer.errors
        assert "cpf" in serializer.errors
        assert "email" in serializer.errors

    def test_serializer_cpf_duplicado(self, db, acionista_sample):
        data = {
            "nome": "Outro Acionista",
            "cpf": acionista_sample.cpf,
            "email": "outro@example.com"
        }
        
        serializer = AcionistaSerializer(data=data)
        assert not serializer.is_valid()
        assert "cpf" in serializer.errors

    def test_serializer_email_duplicado(self, db, acionista_sample):
        data = {
            "nome": "Outro Acionista",
            "cpf": "98765432109",
            "email": acionista_sample.email
        }
        
        serializer = AcionistaSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors


class TestParticipacaoSerializer:
    def test_serializer_valido(self, db, empresa_sample, acionista_sample):
        data = {
            "acionista": acionista_sample.id,
            "empresa": empresa_sample.id,
            "percentual": "25.50"
        }
        
        serializer = ParticipacaoSerializer(data=data)
        assert serializer.is_valid()
        
        participacao = serializer.save()
        assert participacao.acionista == acionista_sample
        assert participacao.empresa == empresa_sample
        assert participacao.percentual == Decimal("25.50")

    def test_serializer_deserializacao(self, participacao_sample):
        serializer = ParticipacaoSerializer(participacao_sample)
        data = serializer.data
        
        assert data["acionista"] == participacao_sample.acionista.id
        assert data["empresa"] == participacao_sample.empresa.id
        assert data["percentual"] == str(participacao_sample.percentual)
        assert data["acionista_nome"] == participacao_sample.acionista.nome
        assert data["empresa_nome"] == participacao_sample.empresa.nome

    def test_serializer_get_acionista_nome(self, participacao_sample):
        serializer = ParticipacaoSerializer(participacao_sample)
        assert serializer.data["acionista_nome"] == participacao_sample.acionista.nome

    def test_serializer_get_empresa_nome(self, participacao_sample):
        serializer = ParticipacaoSerializer(participacao_sample)
        assert serializer.data["empresa_nome"] == participacao_sample.empresa.nome

    def test_serializer_valida_percentual_negativo(self, db, empresa_sample, acionista_sample):
        data = {
            "acionista": acionista_sample.id,
            "empresa": empresa_sample.id,
            "percentual": "-10.00"
        }
        
        serializer = ParticipacaoSerializer(data=data)
        assert not serializer.is_valid()
        assert "percentual" in serializer.errors

    def test_serializer_valida_percentual_maior_100(self, db, empresa_sample, acionista_sample):
        data = {
            "acionista": acionista_sample.id,
            "empresa": empresa_sample.id,
            "percentual": "150.00"
        }
        
        serializer = ParticipacaoSerializer(data=data)
        assert not serializer.is_valid()
        assert "percentual" in serializer.errors

    def test_serializer_valida_percentual_zero(self, db, empresa_sample, acionista_sample):
        data = {
            "acionista": acionista_sample.id,
            "empresa": empresa_sample.id,
            "percentual": "0.00"
        }
        
        serializer = ParticipacaoSerializer(data=data)
        assert not serializer.is_valid()
        assert "percentual" in serializer.errors

    def test_serializer_campos_obrigatorios(self, db):
        serializer = ParticipacaoSerializer(data={})
        assert not serializer.is_valid()
        assert "acionista" in serializer.errors
        assert "empresa" in serializer.errors
        assert "percentual" in serializer.errors

