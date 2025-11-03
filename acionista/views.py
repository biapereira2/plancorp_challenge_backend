from django.shortcuts import render
from rest_framework import viewsets
from .models import Acionista
from .serializers import AcionistaSerializer

class AcionistaView(viewsets.ModelViewSet):
    queryset = Acionista.objects.all()
    serializer_class = AcionistaSerializer
    




