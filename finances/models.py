import uuid

from django.db import models
from django.contrib.auth.models import User

from accounts.models import Account


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=[("entrada", "entrada"), ("saida", "saida")])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Transacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conta = models.ForeignKey(Account, on_delete=models.CASCADE)  # <-- NOVO
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255)
    data = models.DateField()
    recorrente = models.BooleanField(default=False)


    parcelas_totais = models.IntegerField(null=True, blank=True)
    parcela_atual = models.IntegerField(null=True, blank=True)
    compra_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    def __str__(self):
        return f"{self.descricao} - {self.valor}"
