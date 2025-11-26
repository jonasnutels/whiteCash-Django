from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transacao, Account  # ajuste caso o nome esteja diferente

@receiver(post_save, sender=Transacao)
def atualizar_saldo(sender, instance, created, **kwargs):
    if not created:
        return  # só executa quando a transação é criada

    conta = instance.conta
    tipo = instance.categoria.tipo

    if tipo == "entrada":
        conta.saldo_atual += instance.valor
    else:
        conta.saldo_atual -= instance.valor

    conta.save()
