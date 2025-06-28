from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from VigilanceAPP.vigilance_permissions import IsEmpresaOwner
from .models import Comprovante, Cliente, ConfiguracaoComprovante, Empresa, Rondas, Titulo, UserEmpresa
from .serializers import ComprovanteSerializer, ClienteSerializer, ConfiguracaoComprovanteSerializer, EmpresaSerializer, RondasSerializer, TituloSerializer, UserSerializer
from .filters import ComprovanteFilter, ClienteFilter, TituloFilter
from django.db.models.functions import Lower
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from . import utils
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.utils.timezone import now
from django.db.models import Sum
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User  



class EmpresaCreateView(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer



class ClientePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ClientesCreateView(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = ClientePagination
    filterset_class = ClienteFilter

    def get_queryset(self):
        empresa_ativa = UserEmpresa.objects.filter(user=self.request.user, is_active=True).first()
        if empresa_ativa:
            return Cliente.objects.filter(empresa=empresa_ativa.empresa)
        return Cliente.objects.none()


    def perform_create(self, serializer):
        try:
            empresa_ativa = UserEmpresa.get_empresa_ativa(self.request.user)
            if not empresa_ativa:
                raise DRFValidationError({"Detail" : "Nenhuma empresa ativa associada"})
            serializer.save(empresa=empresa_ativa.empresa)
        except DjangoValidationError as e:
            raise DRFValidationError({"detail": e.messages})


class TituloPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class TitulosCreateView(viewsets.ModelViewSet):
    serializer_class = TituloSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = TituloPagination
    filterset_class = TituloFilter

    def get_queryset(self):
        
        user = self.request.user
        user_empresa = UserEmpresa.objects.filter(user=user, is_active=True).first()

        if not user_empresa:
            return Titulo.objects.none()
        
        return Titulo.objects.filter(empresa=user_empresa.empresa)



class ComprovanteCreateView(viewsets.ModelViewSet):
    serializer_class = ComprovanteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComprovanteFilter

    def get_queryset(self):
        user = self.request.user
        user_empresa = UserEmpresa.objects.filter(user=user, is_active=True).first()
        
        if not user_empresa:
            return Comprovante.objects.none()
        
        return Comprovante.objects.filter(empresa=user_empresa.empresa)




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
    serializer_class = ConfiguracaoComprovanteSerializer

    def get_queryset(self):
        empresa_ativa = UserEmpresa.get_empresa_ativa(self.request.user)
        if empresa_ativa:
            return ConfiguracaoComprovante.objects.filter(empresa=empresa_ativa.empresa)
        return ConfiguracaoComprovante.objects.none()
    
    def perform_create(self, serializer):
        try:
            empresa_ativa = UserEmpresa.get_empresa_ativa(self.request.user)
            if not empresa_ativa:
                raise DRFValidationError({"Detail" : "Nenhuma empresa ativa associada"})
            serializer.save(empresa=empresa_ativa.empresa)
        except DjangoValidationError as e:
            raise DRFValidationError({"detail": e.messages})




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
    user = request.user
    empresa_obj = UserEmpresa.get_empresa_ativa(user)
    if not empresa_obj:
        return Response({'Detail':'Usuário não possui empresa vinculada.'})
    empresa_id = empresa_obj.empresa_id

    enderecos = (
        Cliente.objects.filter(empresa_id=empresa_id)
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
    
    serializer_class = RondasSerializer
    permission_classes = [IsEmpresaOwner]

    def get_queryset(self):
        user = self.request.user
        empresa_obj = UserEmpresa.get_empresa_ativa(user)
        empresa_id = empresa_obj.empresa_id

        if empresa_obj:
            return Rondas.objects.filter(empresa_id=empresa_id)
        return Rondas.objects.none()



@api_view(['GET'])
def dashboard_data(request):
    hoje = now().date()
    user = request.user
    empresa_obj = UserEmpresa.get_empresa_ativa(user)
    if not empresa_obj:
        return Response({'detail': 'Usuário não possui empresa vinculada!'})
    empresa_id = empresa_obj.empresa_id

    total_clientes = Cliente.objects.filter(ativo=True, empresa_id=empresa_id).count()

    cobrancas_totais = Titulo.objects.filter(empresa_id=empresa_id).aggregate(total=Sum('valor'))['total'] or 0

    recebido_hoje = Titulo.objects.filter(quitado=True, pagamento=hoje, empresa_id=empresa_id).aggregate(total=Sum('valor'))['total'] or 0

    
    recebimentos = []
    for i in range(7):
        dia = hoje - timedelta(days=i)
        total_dia = Titulo.objects.filter(
            quitado=True,
            pagamento=dia,
            empresa_id=empresa_id
        ).aggregate(total=Sum('valor'))['total'] or 0
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
    

class UserListCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.user

        empresa_ativa = (
            UserEmpresa.objects.filter(user=user, is_active=True)
            .select_related('empresa')
            .first()
        )
        empresa_data = {
            "id" : empresa_ativa.empresa.id,
            "nome" : empresa_ativa.empresa.nome,
        } if empresa_ativa else None
        


        response_data = {
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
            'user_id': user.id,
            'username': user.username,
            'empresa_ativa': empresa_data
        }
        
        return Response(response_data)