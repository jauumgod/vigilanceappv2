from .models import ConfiguracaoComprovante, Rondas, Titulo, Cliente, Comprovante
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ClienteSerializer(serializers.ModelSerializer):
    # vencimento = serializers.SerializerMethodField()
    titulos_em_aberto = serializers.SerializerMethodField()
    todos_titulos_quitados = serializers.SerializerMethodField()

    
    class Meta:
        model = Cliente
        unique_together = ('nome', 'telefone')
        fields = '__all__'

    def get_titulos_em_aberto(self, obj):
        return obj.titulos_em_aberto()

    def get_todos_titulos_quitados(self, obj):
        return obj.todos_titulos_quitados()


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




class ComprovanteSerializer(serializers.ModelSerializer):
    titulo = TituloSerializer()
    class Meta:
        model = Comprovante
        fields = '__all__' # ou liste os campos, incluindo 'logo'

    

class ConfiguracaoComprovanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoComprovante
        fields = '__all__'

class RondasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rondas
        fields = '__all__'

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # criptografa a senha
        user.save()
        return user

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adicione campos personalizados ao token
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
        }
        return data