from django.db import models
from django.core.validators import MinLengthValidator

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(unique=True, max_length=14, validators=[MinLengthValidator(14)])
    endereco = models.CharField(max_length=255)
    data_fundacao = models.DateField()

    def __str__(self):
        return self.nome
