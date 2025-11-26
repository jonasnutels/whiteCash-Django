import uuid
from rest_framework import serializers
from .models import Categoria, Transacao, Account


# ----------------------------
# Categoria
# ----------------------------
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome", "tipo"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Categoria.objects.create(usuario=user, **validated_data)


# ----------------------------
# Transação normal
# ----------------------------
class TransacaoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    conta = serializers.IntegerField(write_only=True)  # receber conta_id
    conta_nome = serializers.CharField(source="conta.nome", read_only=True)
    tipo = serializers.CharField(source="categoria.tipo", read_only=True)
    class Meta:
        model = Transacao
        fields = [
            "id",
            "categoria",
            "categoria_nome",
            "conta",          # conta_id enviado
            "conta_nome",     # nome da conta retornado
            "valor",
            "descricao",
            "data",
            "recorrente",
            "tipo",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        # Extrair conta_id
        conta_id = validated_data.pop("conta")
        conta = Account.objects.get(id=conta_id, usuario=user)

        return Transacao.objects.create(
            usuario=user, conta=conta, **validated_data
        )


# ----------------------------
# Criação de transação parcelada
# ----------------------------
class CriarParceladoSerializer(serializers.Serializer):
    categoria = serializers.IntegerField()
    conta = serializers.IntegerField()  # conta_id
    valor_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    parcelas_totais = serializers.IntegerField()
    descricao = serializers.CharField()
    data_inicial = serializers.DateField()
    tipo = serializers.CharField(source="categoria.tipo", read_only=True)
    def create(self, validated_data):
        user = self.context["request"].user

        categoria_id = validated_data["categoria"]
        conta_id = validated_data["conta"]
        total = validated_data["valor_total"]
        qtd = validated_data["parcelas_totais"]
        descricao = validated_data["descricao"]
        data = validated_data["data_inicial"]

        # Validar categoria e conta do usuário
        categoria = Categoria.objects.get(id=categoria_id, usuario=user)
        conta = Account.objects.get(id=conta_id, usuario=user)

        valor_parcela = total / qtd
        compra_id = uuid.uuid4()

        transacoes = []

        from datetime import timedelta

        # Criar N parcelas
        for i in range(qtd):
            mes_data = data + timedelta(days=30 * i)

            trans = Transacao.objects.create(
                usuario=user,
                categoria=categoria,
                conta=conta,
                valor=valor_parcela,
                descricao=f"{descricao} - Parcela {i + 1}/{qtd}",
                data=mes_data,
                recorrente=False,
                tipo="saida",
                parcelas_totais=qtd,
                parcela_atual=i + 1,
                compra_uuid=compra_id,
            )

            transacoes.append(trans)

        return transacoes
