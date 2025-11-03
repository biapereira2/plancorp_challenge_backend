from rest_framework import serializers
from .models import Acionista

class AcionistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acionista
        fields = '__all__'