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
            venc = date(hoje.year, hoje.month, 1) + relativedelta(months=i)
            venc = venc.replace(day=instance.vencimento)

            Titulo.objects.create(
                cliente=instance,
                valor=instance.valor,
                vencimento=venc,
                endereco=instance.endereco
            )
