from .models import Titulo, Cliente, Comprovante
from rest_framework import serializers


class TituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titulo
        fields = '__all__' 


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' 


class ComprovanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprovante
        fields = '__all__'  # ou liste os campos, incluindo 'logo'