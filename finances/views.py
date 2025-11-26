from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Categoria, Transacao
from .serializers import CategoriaSerializer, TransacaoSerializer, CriarParceladoSerializer


# ---- CATEGORIAS ----

class CategoriaListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)


class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)


# ---- TRANSAÇÕES ----

class TransacaoListCreateView(generics.ListCreateAPIView):
    serializer_class = TransacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user).order_by("-data")


class TransacaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)
class CriarCompraParceladaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CriarParceladoSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        transacoes = serializer.save()

        return Response({
            "detail": "Compra parcelada criada com sucesso.",
            "parcelas": len(transacoes),
        })