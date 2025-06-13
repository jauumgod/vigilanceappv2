from django.db import models, transaction
import re
from django.core.exceptions import ValidationError
import uuid


class Rondas(models.Model):
    nome = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    telefone = models.CharField(max_length=14)
    

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=14)
    endereco = models.CharField(max_length=255, null=True, blank=True) #bairro
    cep = models.CharField(max_length=15, null=True, blank=True)
    numero_casa = models.IntegerField(null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    valor = models.FloatField(default=0)
    vencimento = models.IntegerField(default=1)
    parcelas = models.IntegerField(default=12)
    ativo = models.BooleanField(default=True)
    rondas = models.ForeignKey(
        Rondas,on_delete=models.CASCADE,
        related_name='rondas',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome
    
# class CodigoSequencial(models.Model):
#     last_code = models.IntegerField(default=1)

#     def gerar_codigo(self):
#         self.last_code += 1
#         self.save()
#         return f"CMP-{self.last_code:06d}"


class Titulo(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='titulos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()
    pagamento = models.DateField(blank=True, null=True)
    quitado = models.BooleanField(default=False)
    endereco = models.CharField(max_length=255, blank=True)
    numero_casa = models.IntegerField(null=True, blank=True)
    # codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.valor = self.cliente.valor
        self.endereco = self.cliente.endereco

        # if not self.codigo:
        #     for _ in range(5):  # Tenta gerar até 5 vezes
        #         with transaction.atomic():
        #             sequencia = CodigoSequencial.objects.select_for_update().first()
        #             if not sequencia:
        #                 sequencia = CodigoSequencial.objects.create()

        #             novo_codigo = sequencia.gerar_codigo()

        #             if not Titulo.objects.filter(codigo=novo_codigo).exists():
        #                 self.codigo = novo_codigo
        #                 break
        #     else:
        #         raise ValueError("Não foi possível gerar um código único para o título.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente}"


def validate_cnpj(value):
    """
    Valida um número de CNPJ. Aceita apenas números com 14 dígitos.
    """
    cnpj = re.sub(r'\D', '', value)

    if len(cnpj) != 14:
        raise ValidationError('CNPJ deve conter 14 dígitos numéricos.')

    if cnpj in (c * 14 for c in "1234567890"):
        raise ValidationError('CNPJ inválido.')

    def calculate_digit(cnpj_base, weights):
        soma = sum(int(digit) * weight for digit, weight in zip(cnpj_base, weights))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    # Primeiro dígito
    first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    first_digit = calculate_digit(cnpj[:12], first_weights)

    # Segundo dígito
    second_weights = [6] + first_weights
    second_digit = calculate_digit(cnpj[:12] + first_digit, second_weights)

    if cnpj[-2:] != first_digit + second_digit:
        raise ValidationError('CNPJ inválido.')


class ConfiguracaoComprovante(models.Model):
    logo = models.ImageField(upload_to='logos/', blank=True)
    nome_empresa = models.CharField(max_length=255, null=True, blank=True)
    pix = models.IntegerField(unique=True, null=True, blank=True)
    mensagem = models.TextField(null=True, blank=True)
    nome_responsavel = models.CharField(max_length=255, null=True, blank=True)
    cnpj = models.CharField(max_length=255, null=True, blank=True, validators=[validate_cnpj])


    def __str__(self):
        return f"Logo do comprovante - ID {self.id}"


class Comprovante(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='comprovantes')
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE, related_name='comprovantes')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField(auto_now_add=True)
    numero = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.cliente)

    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo_numero = Comprovante.objects.aggregate(maior=models.Max('numero'))['maior']
            self.numero = (ultimo_numero or 0) + 1
        super().save(*args, **kwargs)

    
