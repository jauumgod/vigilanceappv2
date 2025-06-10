from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=14)
    endereco = models.CharField(max_length=255)
    valor = models.FloatField(default=0)
    vencimento = models.IntegerField(default=1)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Titulo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='titulos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()
    pagamento = models.DateField(blank=True, null=True)
    quitado = models.BooleanField(default=False)
    endereco = models.CharField(max_length=255, blank=True)


    def save(self, *args, **kwargs):
        # Sempre pega o valor atualizado do cliente antes de salvar
        self.valor = self.cliente.valor
        self.endereco = self.cliente.endereco
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente}"



class ConfiguracaoComprovante(models.Model):
    logo = models.ImageField(upload_to='logos/', blank=True)

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