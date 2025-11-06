# 🏢 Projeto Plancorp

Aplicação desenvolvida com **Django REST Framework** (backend) e **React** (frontend) para o gerenciamento de **acionistas**, **empresas** e **participações acionárias**.  
O sistema permite o cadastro, edição e exclusão de acionistas e empresas, além do registro de compras de ações entre eles.

---

## 🚀 Tecnologias Utilizadas

### **Backend**
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)

---

## ⚙️ Funcionalidades

### 🔹 **Empresas**
- Criar novas empresas com nome, CNPJ, endereço e data de fundação.
- Editar informações de empresas existentes.
- Excluir empresas.
- Atualização automática do percentual de ações vendidas conforme as participações registradas.

### 🔹 **Acionistas**
- Cadastrar novos acionistas com nome, CPF, e-mail e data de cadastro.
- Editar e excluir acionistas.
- Validação automática de campos como CPF e e-mail.

### 🔹 **Participações (Compra de Ações)**
- Registrar a compra de ações de um acionista em uma empresa.
- Atualização automática do percentual de ações da empresa.
- Validação para garantir que o percentual informado esteja entre **0% e 100%**.
- Efeito cascata: se um acionista ou empresa for deletado, as participações relacionadas são removidas corretamente.

---

## 🖥️ Como executar o projeto
- Clone o repositório
```bash
git clone https://github.com/biapereira2/plancorp_challenge_backend.git
cd projeto_plancorp
```
- Configure o ambiente virtual
```bash
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
O backend será iniciado em: http://127.0.0.1:8000/

--- 

## 📚 Principais Endpoints
- /empresa/empresas/ - 	Criar empresas e listar todas as empresas cadastradas
- /empresa/empresas/{id}/	- Deletar uma empresa, retornar os dados de uma empresa e atualizar os dados existentes
- /acionista/acionistas/ - Criar acionistas e listar todos os acionistas cadastrados
- /acionista/acionistas/{id}/ - Deletar um acionista, retornar os dados de um acionista e atualizar os dados existentes
- /participacao/participacoes/ - Registrar uma participação e listar todas as participações
- /participacao/participacoes/{id}/ - Retornar detalhes de uma participação

## 🧪 Testes Automatizados

Os testes foram implementados com **pytest** para validar o comportamento dos modelos e das regras de negócio.

Para executar os testes:

```bash
pytest
```



