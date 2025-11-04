from django.shortcuts import render
from rest_framework import viewsets
from .models import Acionista, Participacao
from .serializers import AcionistaSerializer, ParticipacaoSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum


class AcionistaView(viewsets.ModelViewSet):
    queryset = Acionista.objects.all()
    serializer_class = AcionistaSerializer
    

class ParticipacaoViewSet(viewsets.ModelViewSet):
    queryset = Participacao.objects.all()
    serializer_class = ParticipacaoSerializer

    def criar(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            empresa = serializer.validated_data['empresa']
            total_percentual = Participacao.objects.filter(empresa=empresa).aggregate(total=Sum('percentual'))['total'] or 0
            novo_percentual = serializer.validated_data['percentual']

            if total_percentual + novo_percentual > 100:
                return Response({"error": "O percentual total não pode exceder 100%.."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def atualizar(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        empresa = instance.empresa

        if serializer.is_valid():
            total_percentual = Participacao.objects.filter(empresa=empresa).exclude(id=instance.id).aggregate(total=Sum('percentual'))['total'] or 0
            novo_percentual = serializer.validated_data.get('percentual', instance.percentual)

            if total_percentual + novo_percentual > 100:
                return Response({"error": "O percentual total não pode exceder 100%."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def deletar(self, request, *args, **kwargs):
        instance = self.get_object()
        empresa = instance.empresa
        empresa.percentual_vendido -= instance.percentual
        empresa.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)




