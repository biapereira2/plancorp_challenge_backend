import pytest
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
import json
from empresa.models import Empresa


@pytest.fixture
def api_client():
    return APIClient()


class TestEmpresaViewSet:
    def test_listar_empresas(self, api_client, empresa_sample):
        url = "/empresa/empresas/"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["nome"] == empresa_sample.nome

    def test_criar_empresa(self, api_client, db):
        url = "/empresa/empresas/"
        data = {
            "nome": "Nova Empresa LTDA",
            "cnpj": "11111111111111",
            "endereco": "Rua Nova, 789",
            "data_fundacao": "2021-01-01"
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["nome"] == "Nova Empresa LTDA"
        assert Empresa.objects.filter(nome="Nova Empresa LTDA").exists()

    def test_obter_empresa(self, api_client, empresa_sample):
        url = f"/empresa/empresas/{empresa_sample.id}/"
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nome"] == empresa_sample.nome
        assert response.data["cnpj"] == empresa_sample.cnpj

    def test_atualizar_empresa(self, api_client, empresa_sample):
        url = f"/empresa/empresas/{empresa_sample.id}/"
        data = {
            "nome": "Empresa Atualizada",
            "cnpj": empresa_sample.cnpj,
            "endereco": "Novo Endereço, 999",
            "data_fundacao": empresa_sample.data_fundacao.isoformat()
        }
        
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nome"] == "Empresa Atualizada"
        empresa_sample.refresh_from_db()
        assert empresa_sample.nome == "Empresa Atualizada"

    def test_atualizar_empresa_parcial(self, api_client, empresa_sample):
        url = f"/empresa/empresas/{empresa_sample.id}/"
        data = {
            "nome": "Nome Atualizado"
        }
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nome"] == "Nome Atualizado"
        empresa_sample.refresh_from_db()
        assert empresa_sample.nome == "Nome Atualizado"

    def test_deletar_empresa(self, api_client, empresa_sample):
        url = f"/empresa/empresas/{empresa_sample.id}/"
        empresa_id = empresa_sample.id
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Empresa.objects.filter(id=empresa_id).exists()

    def test_criar_empresa_cnpj_duplicado(self, api_client, empresa_sample):
        url = "/empresa/empresas/"
        data = {
            "nome": "Outra Empresa",
            "cnpj": empresa_sample.cnpj,
            "endereco": "Outro Endereço",
            "data_fundacao": "2020-01-01"
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_criar_empresa_dados_invalidos(self, api_client, db):
        url = "/empresa/empresas/"
        data = {
            "nome": "",
            "cnpj": "123",
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

