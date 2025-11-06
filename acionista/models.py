from django.db import models
from django.core.validators import MinLengthValidator

from empresa.models import Empresa

class Acionista(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(unique=True, max_length=11, validators=[MinLengthValidator(11)])
    email = models.EmailField(unique=True, max_length=254)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Participacao(models.Model):
    acionista = models.ForeignKey(Acionista, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    percentual = models.DecimalField(max_digits=5, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.acionista.nome} possui {self.percentual}% de {self.empresa.nome}"