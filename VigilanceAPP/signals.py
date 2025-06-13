from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cliente, Titulo
from datetime import date
from dateutil.relativedelta import relativedelta

@receiver(post_save, sender=Cliente)
def criar_titulos_para_cliente(sender, instance, created, **kwargs):
    if created:
        hoje = date.today()
        for i in range(instance.parcelas):
            # Calcula mês de vencimento + i meses
            venc = hoje + relativedelta(months=i)

            # Ajusta o dia de vencimento
            try:
                venc = venc.replace(day=instance.vencimento)
            except ValueError:
                # Se o dia não existe (ex: 30 de fevereiro), coloca o último dia do mês
                venc = venc.replace(day=1) + relativedelta(months=1) - relativedelta(days=1)

            Titulo.objects.create(
                cliente=instance,
                valor=instance.valor,
                vencimento=venc,
                endereco=instance.endereco
            )


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cliente, Titulo

@receiver(post_save, sender=Cliente)
def desativar_titulos_quando_cliente_desativado(sender, instance, **kwargs):
    if not instance.ativo:  # Se cliente foi desativado
        # Desativa os títulos relacionados
        Titulo.objects.filter(cliente=instance).update(ativo=False)