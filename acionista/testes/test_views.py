import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from acionista.models import Acionista, Participacao
from empresa.models import Empresa


@pytest.fixture
def api_client():
    return APIClient()


class TestAcionistaViewSet:
    def test_listar_acionistas(self, api_client, acionista_sample):
        url = "/acionista/acionistas/"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["nome"] == acionista_sample.nome

    def test_criar_acionista(self, api_client, db):
        url = "/acionista/acionistas/"
        data = {
            "nome": "Novo Acionista",
            "cpf": "11111111111",
            "email": "novo@example.com"
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["nome"] == "Novo Acionista"
        assert Acionista.objects.filter(nome="Novo Acionista").exists()

    def test_obter_acionista(self, api_client, acionista_sample):
        url = f"/acionista/acionistas/{acionista_sample.id}/"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nome"] == acionista_sample.nome
        assert response.data["cpf"] == acionista_sample.cpf

    def test_atualizar_acionista(self, api_client, acionista_sample):
        url = f"/acionista/acionistas/{acionista_sample.id}/"
        data = {
            "nome": "Acionista Atualizado",
            "cpf": acionista_sample.cpf,
            "email": "atualizado@example.com"
        }
        
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nome"] == "Acionista Atualizado"
        acionista_sample.refresh_from_db()
        assert acionista_sample.nome == "Acionista Atualizado"

    def test_deletar_acionista(self, api_client, acionista_sample):
        url = f"/acionista/acionistas/{acionista_sample.id}/"
        acionista_id = acionista_sample.id
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Acionista.objects.filter(id=acionista_id).exists()

    def test_criar_acionista_cpf_duplicado(self, api_client, acionista_sample):
        url = "/acionista/acionistas/"
        data = {
            "nome": "Outro Acionista",
            "cpf": acionista_sample.cpf,
            "email": "outro@example.com"
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_criar_acionista_email_duplicado(self, api_client, acionista_sample):
        url = "/acionista/acionistas/"
        data = {
            "nome": "Outro Acionista",
            "cpf": "99999999999",
            "email": acionista_sample.email
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestParticipacaoViewSet:
    def test_listar_participacoes(self, api_client, participacao_sample):
        url = "/acionista/participacoes/"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["acionista"] == participacao_sample.acionista.id

    def test_criar_participacao(self, api_client, empresa_sample, acionista_sample):
        url = "/acionista/participacoes/"
        data = {
            "acionista": acionista_sample.id,
            "empresa": empresa_sample.id,
            "percentual": "30.00"
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["percentual"] == "30.00"
        assert Participacao.objects.filter(
            acionista=acionista_sample,
            empresa=empresa_sample
        ).exists()

    def test_obter_participacao(self, api_client, participacao_sample):
        url = f"/acionista/participacoes/{participacao_sample.id}/"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["acionista"] == participacao_sample.acionista.id
        assert response.data["empresa"] == participacao_sample.empresa.id
        assert response.data["acionista_nome"] == participacao_sample.acionista.nome
        assert response.data["empresa_nome"] == participacao_sample.empresa.nome

    def test_atualizar_participacao(self, api_client, participacao_sample):
        url = f"/acionista/participacoes/{participacao_sample.id}/"
        data = {
            "acionista": participacao_sample.acionista.id,
            "empresa": participacao_sample.empresa.id,
            "percentual": "35.00"
        }
        
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["percentual"] == "35.00"
        participacao_sample.refresh_from_db()
        assert participacao_sample.percentual == Decimal("35.00")

    def test_deletar_participacao(self, api_client, participacao_sample):
        url = f"/acionista/participacoes/{participacao_sample.id}/"
        participacao_id = participacao_sample.id
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Participacao.objects.filter(id=participacao_id).exists()

    def test_criar_participacao_percentual_excede_100(self, api_client, empresa_sample, acionista_sample):
        Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("60.00")
        )
        
        url = "/acionista/participacoes/"
        data = {
            "acionista": acionista_sample.id,
            "empresa": empresa_sample.id,
            "percentual": "50.00"
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "percentual" in str(response.data) or "exceder" in str(response.data).lower()

    def test_atualizar_participacao_percentual_excede_100(self, api_client, empresa_sample, acionista_sample, acionista_sample_2):
        participacao1 = Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("40.00")
        )
        
        participacao2 = Participacao.objects.create(
            acionista=acionista_sample_2,
            empresa=empresa_sample,
            percentual=Decimal("30.00")
        )

        url = f"/acionista/participacoes/{participacao1.id}/"
        data = {
            "acionista": participacao1.acionista.id,
            "empresa": participacao1.empresa.id,
            "percentual": "80.00"
        }
        
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "percentual" in str(response.data) or "exceder" in str(response.data).lower()

    def test_criar_participacao_percentual_valido_total_100(self, api_client, empresa_sample, acionista_sample, acionista_sample_2):
        Participacao.objects.create(
            acionista=acionista_sample,
            empresa=empresa_sample,
            percentual=Decimal("60.00")
        )
        
        url = "/acionista/participacoes/"
        data = {
            "acionista": acionista_sample_2.id,
            "empresa": empresa_sample.id,
            "percentual": "40.00"
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Participacao.objects.filter(empresa=empresa_sample).count() == 2

