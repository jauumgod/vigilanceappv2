from django.db import models, transaction
import re
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import uuid

User = get_user_model()


class Empresa(models.Model):

    PESSOA_CHOICES = [
        ('F', 'Física'),
        ('J', 'Jurídica'),
    ]
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=15, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=18)
    pessoa = models.CharField(
        max_length=1,
        choices=PESSOA_CHOICES,
        default='F'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class UserEmpresa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empresas')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    @staticmethod
    def get_empresa_ativa(user):
        return user.empresas.filter(is_active=True).first()

    class Meta:
        unique_together = ('user','empresa')

    def __str__(self):
        return self.empresa.nome

class Rondas(models.Model):
    nome = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    telefone = models.CharField(max_length=14)
    empresa = models.ForeignKey(Empresa,
                                on_delete=models.CASCADE,
                                related_name='rondas_empresas'
                            )
    
    def __str__(self):
        return self.nome
    
#Verificação de Nome + Telefone
def validar_cpf(value):
    cpf = ''.join(filter(str.isdigit, value))
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 dígitos.')

    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido.')

    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if cpf[-2:] != f"{digito1}{digito2}":
        raise ValidationError('CPF inválido.')
    

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=12, null=True, blank=True, validators=[validar_cpf])
    telefone = models.CharField(max_length=14)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=15, null=True, blank=True)
    numero_casa = models.IntegerField(null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    valor = models.FloatField(default=0)
    vencimento = models.IntegerField(default=1)
    parcelas = models.IntegerField(default=12)
    ativo = models.BooleanField(default=True)
    rondas = models.ForeignKey(
        Rondas, on_delete=models.CASCADE,
        related_name='rondas',
        null=True,
        blank=True
    )
    empresa = models.ForeignKey(Empresa,
                                on_delete=models.CASCADE,
                                related_name='cliente_empresas'
                            )

    

    def __str__(self):
        return self.nome

    def clean(self):
        # Verifica se já existe outro cliente com mesmo nome e telefone
        if Cliente.objects.exclude(id=self.id).filter(nome=self.nome, telefone=self.telefone).exists():
            raise ValidationError("Já existe um cliente com este nome e telefone.")

    def save(self, *args, **kwargs):
        self.full_clean()  # chama clean() antes de salvar
        super().save(*args, **kwargs)

    def titulos_em_aberto(self):
        return self.titulos.filter(quitado=False).count()

    def todos_titulos_quitados(self):
        return not self.titulos.filter(quitado=False).exists()
    
class CodigoSequencial(models.Model):
    last_code = models.IntegerField(default=1)

    def gerar_codigo(self):
        self.last_code += 1
        self.save()
        return f"RZTCH-{self.last_code:06d}"


class Titulo(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='titulos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()
    pagamento = models.DateField(blank=True, null=True)
    quitado = models.BooleanField(default=False)
    endereco = models.CharField(max_length=255, blank=True)
    numero_casa = models.IntegerField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    codigo = models.CharField(max_length=255, blank=True, editable=False)
    empresa = models.ForeignKey(Empresa,
                                on_delete=models.CASCADE,
                                related_name='titulo_empresas'
                            )

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.valor in [None, '']:
                self.valor = self.cliente.valor
            if self.endereco in [None, '']:
                self.endereco = self.cliente.endereco
            if self.numero_casa in [None, '']:
                self.numero_casa = self.cliente.numero_casa

        if not self.codigo:
            sequencia, _ = CodigoSequencial.objects.get_or_create(id=1)
            self.codigo = sequencia.gerar_codigo()

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
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    nome_empresa = models.CharField(max_length=255, null=True, blank=True)
    pix = models.CharField(max_length=255, null=True, blank=True)
    mensagem = models.TextField(null=True, blank=True)
    nome_responsavel = models.CharField(max_length=255, null=True, blank=True)
    cnpj = models.CharField(max_length=255, null=True, blank=True, validators=[validate_cnpj])
    criado_em = models.DateField(auto_now_add=True, blank=True, null=True)
    empresa = models.ForeignKey(Empresa,
                                on_delete=models.CASCADE,
                                related_name='config_empresas'
                            )
    
    def __str__(self):
        return f"Logo do comprovante - ID {self.id}"


class Comprovante(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='comprovantes')
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE, related_name='comprovantes')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField(auto_now_add=True)
    numero = models.PositiveIntegerField(unique=True, blank=True, null=True)
    empresa = models.ForeignKey(Empresa,
                                on_delete=models.CASCADE,
                                related_name='comprovante_empresas'
                            )

    def __str__(self):
        return str(self.cliente)

    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo_numero = Comprovante.objects.aggregate(maior=models.Max('numero'))['maior']
            self.numero = (ultimo_numero or 0) + 1
        super().save(*args, **kwargs)

#Melhoria futura para Cobranças
  
# class Cobranca(models.Model):
#     email = models.EmailField()
    # empresa = models.ForeignKey(Empresa,
    #                             on_delete=models.CASCADE,
    #                             related_name='cobranca_empresa'
    #                         )

#     def __str__(self):
#         return self.email