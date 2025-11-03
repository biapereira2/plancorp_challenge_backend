from django.db import models
from django.core.validators import MinLengthValidator

class Acionista(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(unique=True, max_length=11, validators=[MinLengthValidator(11)])
    email = models.EmailField(unique=True, max_length=254)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
