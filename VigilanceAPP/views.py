from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Comprovante, Cliente, ConfiguracaoComprovante, Titulo
from .serializers import ComprovanteSerializer, ClienteSerializer, ConfiguracaoComprovanteSerializer, TituloSerializer
from .filters import ComprovanteFilter, ClienteFilter, TituloFilter



class ClientesCreateView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClienteFilter



class TitulosCreateView(viewsets.ModelViewSet):
    queryset = Titulo.objects.all()
    serializer_class = TituloSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TituloFilter


class ComprovanteCreateView(viewsets.ModelViewSet):
    queryset = Comprovante.objects.all()
    serializer_class = ComprovanteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComprovanteFilter

class ComprovanteListView(APIView):
    def get(self, request):
        comprovantes = Comprovante.objects.all()
        serializer = ComprovanteSerializer(comprovantes, many=True)
        return Response(serializer.data)

    def post(self, request):
        titulo_id = request.data.get('titulo_id')
        valor_pago = request.data.get('valor_pago')

        if not titulo_id or not valor_pago:
            return Response({"error": "titulo_id e valor_pago são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            titulo = Titulo.objects.get(id=titulo_id)
        except Titulo.DoesNotExist:
            return Response({"error": "Título não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        comprovante = Comprovante(
            cliente=titulo.cliente,
            titulo=titulo,
            valor_pago=valor_pago
        )
        comprovante.save()

        return Response({
            "id": comprovante.id,
            "numero": comprovante.numero,
            "cliente": str(comprovante.cliente),
            "valor_pago": str(comprovante.valor_pago),
            "data_pagamento": comprovante.data_pagamento
        }, status=status.HTTP_201_CREATED)


class ConfiguracaoComprovanteViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoComprovante.objects.all()
    serializer_class = ConfiguracaoComprovanteSerializer

    class Meta:
        model = Comprovante
        fields = '__all__' 


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import utils
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@api_view(['POST'])
@permission_classes([AllowAny])
def gerar_titulos(request):
    try:
        resultado = utils.criar_titulos()
        return Response({'mensagem': resultado}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'erro': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

from django.db.models.functions import Lower

@api_view(['GET'])
def enderecos_unicos(request):
    enderecos = (
        Cliente.objects
        .values_list('endereco', flat=True)
        .distinct()
        .order_by(Lower('endereco'))
    )
    return Response(sorted(enderecos))

from rest_framework.views import APIView



class LogoComprovanteView(APIView):
    def get(self, request):
        config = ConfiguracaoComprovante.objects.last()  # ou filtre por ID
        serializer = ConfiguracaoComprovanteSerializer(config, context={'request': request})
        return Response(serializer.data)


    
