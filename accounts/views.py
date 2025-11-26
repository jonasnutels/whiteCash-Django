from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from accounts.forms import AccountForm
from accounts.models import Account
from accounts.serializer import AccountSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"detail": "Credenciais inválidas"}, status=400)

        refresh = RefreshToken.for_user(user)

        res = Response({"detail": "Login realizado com sucesso"})

        # Cookies HTTPOnly
        res.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 30,
        )

        res.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 60 * 24 * 7,
        )

        return res
class LogoutView(APIView):
    def post(self, request):
        res = Response({"detail": "Logout realizado"})

        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")

        return res
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "Refresh token não encontrado."}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token
        except Exception as e:
            return Response({"detail": "Refresh token inválido ou expirado."}, status=401)

        # Criar nova resposta
        response = Response({"detail": "Access token renovado com sucesso."})

        # Definir novo access_token no cookie
        response.set_cookie(
            key="access_token",
            value=str(new_access_token),
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 30,  # 30 minutos
        )

        return response
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "superuser": request.user.is_superuser,
        })


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by("-data_criacao")
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Usuário só vê as contas dele.
        """
        return Account.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        """
        Garante que a conta sempre seja criada vinculada ao usuário logado.
        """
        serializer.save(usuario=self.request.user)
