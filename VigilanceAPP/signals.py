from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Cliente, Titulo
from datetime import date
from dateutil.relativedelta import relativedelta
from django.dispatch import receiver
from .models import Cliente, Titulo
from django.utils import timezone

@receiver(post_save, sender=Cliente)
def criar_titulos_para_cliente(sender, instance, created, **kwargs):
    if created:
        hoje = date.today()
        
        faturas_criadas = 0
        mes_offset = 0

        # Continua até criar todas as parcelas
        while faturas_criadas < instance.parcelas:
            venc = hoje + relativedelta(months=mes_offset)
            mes_offset += 1  # incrementa sempre

            try:
                venc = venc.replace(day=instance.vencimento)
            except ValueError:
                venc = venc.replace(day=1) + relativedelta(months=1) - relativedelta(days=1)

            # Só cria se vencimento for no futuro
            if venc >= hoje:
                Titulo.objects.create(
                    cliente=instance,
                    valor=instance.valor,
                    vencimento=venc,
                    endereco=instance.endereco,
                    numero_casa=instance.numero_casa,
                    empresa=instance.empresa
                )
                faturas_criadas += 1





@receiver(post_save, sender=Cliente)
def desativar_titulos_quando_cliente_desativado(sender, instance, **kwargs):
    if not instance.ativo:  # Se cliente foi desativado
        # Desativa os títulos relacionados
        Titulo.objects.filter(cliente=instance).update(ativo=False)


@receiver(pre_save, sender=Cliente)
def atualizar_titulos_futuros(sender, instance, **kwargs):
    if not instance.pk:
        return  # Cliente novo — não há títulos para atualizar ainda

    cliente_antigo = Cliente.objects.get(pk=instance.pk)

    if cliente_antigo.valor != instance.valor or cliente_antigo.parcelas != instance.parcelas:
        hoje = timezone.now().date()
        titulos = Titulo.objects.filter(
            cliente=instance,
            vencimento__gte=hoje,
            ativo=True,
            quitado=False
        )

        for titulo in titulos:
            # Distribui novo valor proporcional às parcelas futuras
            titulo.valor = instance.valor
            titulo.save()