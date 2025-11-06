import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal
from datetime import date
from acionista.models import Acionista, Participacao
from empresa.models import Empresa


class TestAcionistaModel:

    def test_criar_acionista(self, db):
        acionista = Acionista.objects.create(
            nome="João Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        assert acionista.id is not None
        assert acionista.nome == "João Silva"
        assert acionista.cpf == "12345678901"
        assert acionista.email == "joao@example.com"
        assert acionista.data_cadastro is not None

    def test_acionista_str(self, db):
        acionista = Acionista.objects.create(
            nome="João Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        assert str(acionista) == "João Silva"

    def test_cpf_unico(self, db):
        Acionista.objects.create(
            nome="João Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        with pytest.raises(IntegrityError):
            Acionista.objects.create(
                nome="João Silva Segundo",
                cpf="12345678901",
                email="joao2@example.com"
            )

    def test_email_unico(self, db):
        Acionista.objects.create(
            nome="João Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        with pytest.raises(IntegrityError):
            Acionista.objects.create(
                nome="Maria Santos",
                cpf="98765432109",
                email="joao@example.com"
            )

    def test_cpf_min_length(self, db):
        acionista = Acionista(
            nome="João Silva",
            cpf="123456789",
            email="joao@example.com"
        )
        
        with pytest.raises(ValidationError):
            acionista.full_clean()

    def test_email_valido(self, db):
        acionista = Acionista(
            nome="João Silva",
            cpf="12345678901",
            email="email_invalido"
        )
        
        with pytest.raises(ValidationError):
            acionista.full_clean()

    def test_data_cadastro_auto(self, db):
        acionista = Acionista.objects.create(
            nome="João Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        assert acionista.data_cadastro is not None

class TestParticipacaoModel:

    def test_criar_participacao(self, db, empresa_sample, acionista_sample):
        participacao = Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("25.50")
        )
        
        assert participacao.id is not None
        assert participacao.acionista == acionista_sample
        assert participacao.empresa == empresa_sample
        assert participacao.percentual == Decimal("25.50")
        assert participacao.criado_em is not None

    def test_participacao_str(self, db, empresa_sample, acionista_sample):
        participacao = Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("25.50")
        )
        
        expected = f"{acionista_sample.nome} possui {participacao.percentual}% de {empresa_sample.nome}"
        assert str(participacao) == expected

    def test_cascade_delete_acionista(self, db, empresa_sample, acionista_sample):
        participacao = Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("25.50")
        )
        
        participacao_id = participacao.id
        acionista_sample.delete()
        
        assert not Participacao.objects.filter(id=participacao_id).exists()

    def test_cascade_delete_empresa(self, db, empresa_sample, acionista_sample):
        participacao = Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("25.50")
        )
        
        participacao_id = participacao.id
        empresa_sample.delete()
        
        assert not Participacao.objects.filter(id=participacao_id).exists()

    def test_percentual_max_digits(self, db, empresa_sample, acionista_sample):
        participacao = Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("100.00")
        )
        
        assert participacao.percentual == Decimal("100.00")

    def test_criado_em_auto(self, db, empresa_sample, acionista_sample):
        participacao = Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("25.50")
        )
        
        assert participacao.criado_em is not None
