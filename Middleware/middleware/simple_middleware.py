from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import AnonymousUser

class SimpleMiddleware(MiddlewareMixin):
    jwt_auth = JWTAuthentication()

    def process_request(self, request):
        auth_header = request.headers.get("Authorization", "")
        session_token = request.session.get("jwt_token")

        # ✅ Nếu không có header nhưng có token trong session → tự thêm
        if not auth_header and session_token:
            auth_header = f"Bearer {session_token}"
            request.META["HTTP_AUTHORIZATION"] = auth_header

        # Nếu không có token → AnonymousUser
        if not auth_header.startswith("Bearer "):
            request.user = AnonymousUser()
            if request.path.startswith("/admin/"):
                return JsonResponse(
                    {"detail": "Vui lòng vào /jwt-login để nhập token."},
                    status=403
                )
            return None

        token = auth_header.split("Bearer ")[1]
        try:
            validated_token = self.jwt_auth.get_validated_token(token)
            user = self.jwt_auth.get_user(validated_token)
            request.user = user

            if request.path.startswith("/admin/") and not (user.is_staff or user.is_superuser):
                return JsonResponse(
                    {"detail": "Chỉ nhân viên hoặc superadmin được phép vào admin."},
                    status=403
                )

        except TokenError as e:
            # Clear expired token from session
            request.session.pop("jwt_token", None)
            request.session.pop("refresh_token", None)
            
            # If accessing admin, redirect to login page
            if request.path.startswith("/admin/"):
                return JsonResponse({
                    "detail": "Token đã hết hạn. Vui lòng vào /jwt-login để nhập token mới.",
                    "redirect": "/jwt-login/"
                }, status=401)
            
            return JsonResponse({
                "detail": "Token không hợp lệ hoặc đã hết hạn.",
                "error": str(e)
            }, status=401)

        return None
