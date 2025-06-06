import django_filters
from .models import Comprovante, Titulo, Cliente

class TituloFilter(django_filters.FilterSet):
    data_pagamento = django_filters.DateFromToRangeFilter()
    cliente = django_filters.CharFilter(field_name='cliente__nome', lookup_expr='icontains')

    class Meta:
        model = Titulo
        fields = ['cliente', 'vencimento', 'quitado']


class ClienteFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Cliente
        fields = ['nome', 'endereco']


class ComprovanteFilter(django_filters.FilterSet):
    data_pagamento = django_filters.DateFromToRangeFilter()
    cliente = django_filters.CharFilter(field_name='cliente__nome', lookup_expr='icontains')

    class Meta:
        model = Comprovante
        fields = ['cliente', 'data_pagamento']


