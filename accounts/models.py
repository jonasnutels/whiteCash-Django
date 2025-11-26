from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    saldo_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tipo = models.CharField(
        max_length=20,
        choices=[("corrente", "corrente"), ("poupanca", "poupanca"), ("cartao", "cartao")],
        default="corrente"
    )
    cor = models.CharField(max_length=20, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - Saldo: {self.saldo_atual}"
