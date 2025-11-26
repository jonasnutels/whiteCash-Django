from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class JWTRefreshMiddleware(MiddlewareMixin):
    """
    - Se o access_token for válido → segue normal.
    - Se o access_token estiver expirado → tenta renovar usando o refresh_token.
    - Se o refresh_token for válido → cria novo access_token e injeta no cookie.
    - Se ambos falharem → não renova, apenas segue → view vai retornar 401.
    """

    def process_request(self, request):
        request.new_access_token = None  # Usado depois na resposta

        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return None  # sem access_token → segue o fluxo normal

        try:
            # Verifica se o access_token ainda é válido
            AccessToken(access_token)
            return None  # Token válido → segue sem mexer em nada

        except TokenError:
            # Access token expirado → tenta renovar usando refresh_token
            if not refresh_token:
                return None  # Não há refresh para tentar

            try:
                refresh = RefreshToken(refresh_token)
                new_access = refresh.access_token
                request.new_access_token = str(new_access)
            except TokenError:
                pass

        return None

    def process_response(self, request, response):
        """
        Se o process_request gerou new_access_token,
        reescrevemos o cookie automaticamente.
        """
        if hasattr(request, "new_access_token") and request.new_access_token:
            response.set_cookie(
                key="access_token",
                value=request.new_access_token,
                httponly=True,
                secure=False,   # ative secure=True em produção
                samesite="Lax",
                max_age=60 * 30,  # 30 minutos
            )

        return response
