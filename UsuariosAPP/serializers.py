from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuarios
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuarios
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        
        # Faz o hash da senha
        password = validated_data.pop('password')
        hashed_password = make_password(password)

        # Cria o usuário com a senha hasheada
        usuario = Usuarios(**validated_data)
        usuario.password = hashed_password
        usuario.save()

        return usuario


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
    