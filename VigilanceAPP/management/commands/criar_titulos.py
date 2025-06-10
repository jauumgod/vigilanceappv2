from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from calendar import monthrange
from ...models import Titulo, Cliente

class Command(BaseCommand):
    help = 'Cria títulos automaticamente para clientes ativos com dia fixo de vencimento'

    def handle(self, *args, **kwargs):
        hoje = timezone.now().date()
        ano = hoje.year
        mes = hoje.month

        clientes = Cliente.objects.filter(ativo=True).exclude(vencimento=None)
        contador = 0

        for cliente in clientes:
            dia = cliente.vencimento

            # Tenta criar a data de vencimento para o mês atual
            try:
                vencimento = date(ano, mes, dia)
            except ValueError:
                # Caso o dia seja inválido (ex: 31/02), usar último dia do mês
                ultimo_dia = monthrange(ano, mes)[1]
                vencimento = date(ano, mes, ultimo_dia)

            # Se a data já passou, joga para o mês seguinte
            if vencimento < hoje:
                if mes == 12:
                    mes = 1
                    ano += 1
                else:
                    mes += 1
                try:
                    vencimento = date(ano, mes, dia)
                except ValueError:
                    ultimo_dia = monthrange(ano, mes)[1]
                    vencimento = date(ano, mes, ultimo_dia)

            # Verifica se já existe um título com esse vencimento
            if not Titulo.objects.filter(cliente=cliente, vencimento=vencimento).exists():
                Titulo.objects.create(
                    cliente=cliente,
                    valor=0,  # ajuste conforme sua regra
                    vencimento=vencimento,
                    quitado=False,
                    # outros campos se necessário
                )
                self.stdout.write(f'Título criado para {cliente.nome} com vencimento {vencimento}')
                contador += 1

        self.stdout.write(self.style.SUCCESS(f'Títulos criados: {contador}'))



##Comando##

# python manage.py criar_titulos