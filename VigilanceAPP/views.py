from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Comprovante, Cliente, Titulo
from .serializers import ComprovanteSerializer, ClienteSerializer, TituloSerializer
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


class ComprovanteListView(viewsets.ModelViewSet):
    queryset = Comprovante.objects.all()
    serializer_class = ComprovanteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComprovanteFilter
