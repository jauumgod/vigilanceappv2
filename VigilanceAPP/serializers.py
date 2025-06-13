from .models import ConfiguracaoComprovante, Rondas, Titulo, Cliente, Comprovante
from rest_framework import serializers


class TituloSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    cliente_endereco = serializers.CharField(source='cliente.endereco', read_only=True)

    class Meta:
        model = Titulo
        fields = '__all__' 
        extra_kwargs = {
            'valor': {'required': False},
            'vencimento': {'required': False},
            'cliente': {'required': False},
        }


class ClienteSerializer(serializers.ModelSerializer):
    # vencimento = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = '__all__'



class ComprovanteSerializer(serializers.ModelSerializer):
    titulo = TituloSerializer()
    class Meta:
        model = Comprovante
        fields = '__all__' # ou liste os campos, incluindo 'logo'

    

class ConfiguracaoComprovanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoComprovante
        fields = ['id', 'logo']


class RondasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rondas
        fields = '__all__'