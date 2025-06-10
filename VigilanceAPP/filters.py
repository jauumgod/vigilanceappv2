import django_filters
from .models import Comprovante, Titulo, Cliente

class TituloFilter(django_filters.FilterSet):
    vencimento = django_filters.DateFromToRangeFilter()
    nome = django_filters.CharFilter(field_name='cliente__nome', lookup_expr='icontains')
    endereco = django_filters.CharFilter(field_name='cliente__endereco', lookup_expr='icontains')

    class Meta:
        model = Titulo
        fields = ['vencimento', 'nome', 'endereco']


class ClienteFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'vencimento']


class ComprovanteFilter(django_filters.FilterSet):
    data_pagamento = django_filters.DateFromToRangeFilter()
    cliente = django_filters.NumberFilter(field_name='cliente_id')

    class Meta:
        model = Comprovante
        fields = ['cliente', 'data_pagamento']


