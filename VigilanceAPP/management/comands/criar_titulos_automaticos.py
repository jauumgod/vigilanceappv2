from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from VigilanceAPP.models import Titulo, Cliente

class Command(BaseCommand):
    help = 'Cria títulos automaticamente para vencimento daqui 10 dias, para clientes ativos com data de pagamento'

    def handle(self, *args, **kwargs):
        hoje = timezone.now().date()
        data_alvo = hoje + timedelta(days=10)

        clientes = Cliente.objects.filter(ativo=True).exclude(data_pagamento=None)
        contador = 0

        for cliente in clientes:
            # Verifica se já existe título para esse cliente e essa data de vencimento
            existe = Titulo.objects.filter(cliente=cliente, data_vencimento=data_alvo).exists()
            if not existe:
                titulo = Titulo.objects.create(
                    cliente=cliente,
                    valor=0,  # Ajuste conforme sua regra de valor
                    data_vencimento=data_alvo,
                    quitado=False,
                    # outros campos obrigatórios aqui
                )
                self.stdout.write(f'Título criado para cliente {cliente} com vencimento {data_alvo}')
                contador += 1

        self.stdout.write(self.style.SUCCESS(f'Títulos criados: {contador}'))
