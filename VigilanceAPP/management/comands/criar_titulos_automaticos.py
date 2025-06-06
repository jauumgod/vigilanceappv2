from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from VigilanceAPP.models import Titulo

class Command(BaseCommand):
    help = 'Cria títulos automaticamente para vencimentos daqui 10 dias'

    def handle(self, *args, **kwargs):
        hoje = timezone.now().date()
        data_alvo = hoje + timedelta(days=10)

        # Verifique se já existe título com essa data de vencimento, para evitar duplicação
        existe = Titulo.objects.filter(data_vencimento=data_alvo).exists()

        if not existe:
            # Crie o título (preencha os campos obrigatórios)
            titulo = Titulo.objects.create(
                cliente=...,  # Defina o cliente aqui
                valor=...,   # Defina o valor
                data_vencimento=data_alvo,
                quitado=False,
                # outros campos que forem necessários
            )
            self.stdout.write(f'Título criado para vencimento {data_alvo}')
        else:
            self.stdout.write(f'Título para vencimento {data_alvo} já existe')
