from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Pegamos o access_token do cookie
        access_token = request.COOKIES.get("access_token")

        if access_token:
            try:
                validated_token = self.get_validated_token(access_token)
                user = self.get_user(validated_token)
                return (user, validated_token)
            except Exception:
                return None

        # Se não tem cookie, tenta header Authorization normal
        return super().authenticate(request)
