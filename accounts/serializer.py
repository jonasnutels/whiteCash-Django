from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    usuario = serializers.CharField(source='usuario.id', read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "usuario",
            "usuario_nome",
            "nome",
            "saldo_atual",
            "tipo",
            "cor",
            "data_criacao",
        ]
        read_only_fields = ["data_criacao"]
