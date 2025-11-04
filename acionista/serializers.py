from rest_framework import serializers
from .models import Acionista, Participacao

class AcionistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acionista
        fields = '__all__'

class ParticipacaoSerializer(serializers.ModelSerializer):
    acionista_nome = serializers.SerializerMethodField()
    empresa_nome = serializers.SerializerMethodField()

    class Meta:
        model = Participacao
        fields = '__all__'

    def valida_percentual(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError("Percentual deve ser maior que 0 e menor ou igual a 100.")
        return value

    def criar(self, validated_data):
        participacao = super().create(validated_data)
        empresa = participacao.empresa
        empresa.percentual_vendido += participacao.percentual
        empresa.save()
        return participacao

    def atualizar(self, instance, validated_data):
        percentual_anterior = instance.percentual
        instance.empresa.percentual_vendido -= percentual_anterior
        instance.empresa.save()
        instance = super().update(instance, validated_data)
        empresa = instance.empresa
        empresa.percentual_vendido += instance.percentual
        empresa.save()
        return instance

    def deletar(self, instance):
        empresa = instance.empresa
        empresa.percentual_vendido -= instance.percentual
        empresa.save()
        instance.delete()

    def get_acionista_nome(self, obj):
        return obj.acionista.nome

    def get_empresa_nome(self, obj):
        return obj.empresa.nome