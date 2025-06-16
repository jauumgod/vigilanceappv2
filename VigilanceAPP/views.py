from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Comprovante, Cliente, ConfiguracaoComprovante, Rondas, Titulo
from .serializers import ComprovanteSerializer, ClienteSerializer, ConfiguracaoComprovanteSerializer, RondasSerializer, TituloSerializer
from .filters import ComprovanteFilter, ClienteFilter, TituloFilter
from django.db.models.functions import Lower
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import utils
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.utils.timezone import now
from django.db.models import Sum
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError



class ClientePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class ClientesCreateView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = ClientePagination
    filterset_class = ClienteFilter

    def perform_create(self, serializer):
        try:
            serializer.save()
        except DjangoValidationError as e:
            raise DRFValidationError({"detail": e.messages})


class TituloPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class TitulosCreateView(viewsets.ModelViewSet):
    queryset = Titulo.objects.all()
    serializer_class = TituloSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = TituloPagination
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


@api_view(['POST'])
@permission_classes([AllowAny])
def gerar_titulos(request):
    try:
        resultado = utils.criar_titulos()
        return Response({'mensagem': resultado}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'erro': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def enderecos_unicos(request):
    enderecos = (
        Cliente.objects
        .values_list('endereco', flat=True)
        .distinct()
        .order_by(Lower('endereco'))
    )
    return Response(sorted(enderecos))



class LogoComprovanteView(APIView):
    def get(self, request):
        config = ConfiguracaoComprovante.objects.last()  # ou filtre por ID
        serializer = ConfiguracaoComprovanteSerializer(config, context={'request': request})
        return Response(serializer.data)



class RondasCreateView(viewsets.ModelViewSet):
    queryset = Rondas.objects.all()
    serializer_class = RondasSerializer



@api_view(['GET'])
def dashboard_data(request):
    hoje = now().date()

    total_clientes = Cliente.objects.filter(ativo=True).count()

    cobrancas_totais = Titulo.objects.aggregate(total=Sum('valor'))['total'] or 0

    recebido_hoje = Titulo.objects.filter(quitado=True, pagamento=hoje).aggregate(total=Sum('valor'))['total'] or 0

    
    recebimentos = []
    for i in range(7):
        dia = hoje - timedelta(days=i)
        total_dia = Titulo.objects.filter(quitado=True, pagamento=dia).aggregate(total=Sum('valor'))['total'] or 0
        recebimentos.append({
            'data': dia.strftime('%Y-%m-%d'),
            'valor': total_dia
        })

    return Response({
        'clientes_cadastrados': total_clientes,
        'cobrancas_totais': cobrancas_totais,
        'recebido_hoje': recebido_hoje,
        'evolucao_recebimentos': list(reversed(recebimentos))
    })


class UltimaConfiguracaoComprovante(APIView):
    def get(self, request):
        ultima = ConfiguracaoComprovante.objects.last()
        serializer = ConfiguracaoComprovanteSerializer(ultima)
        return Response(serializer.data)