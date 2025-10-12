from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
import json

def jwt_login(request):
    if request.method == "POST":
        token = request.POST.get("token", "").strip()
        refresh_token = request.POST.get("refresh_token", "").strip()

        if token:
            # Validate the token before saving
            jwt_auth = JWTAuthentication()
            try:
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                
                # Lưu token vào session
                request.session["jwt_token"] = token
                if refresh_token:
                    request.session["refresh_token"] = refresh_token
                
                messages.success(request, f"Token đã được lưu cho user: {user.username}! Bạn có thể vào /admin/")
                return redirect("/admin/")
                
            except TokenError as e:
                messages.error(request, f"Token không hợp lệ: {str(e)}")
        else:
            messages.error(request, "Vui lòng nhập token!")

    return render(request, "jwt_login.html")

def refresh_token_view(request):
    """API endpoint to refresh JWT token"""
    if request.method == "POST":
        refresh_token = request.session.get("refresh_token")
        
        if not refresh_token:
            return JsonResponse({
                "error": "Không có refresh token trong session"
            }, status=400)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            
            # Update session with new access token
            request.session["jwt_token"] = new_access_token
            
            return JsonResponse({
                "access_token": new_access_token,
                "message": "Token đã được làm mới thành công"
            })
            
        except TokenError as e:
            # Clear invalid tokens
            request.session.pop("jwt_token", None)
            request.session.pop("refresh_token", None)
            
            return JsonResponse({
                "error": f"Refresh token không hợp lệ: {str(e)}",
                "redirect": "/jwt-login/"
            }, status=401)
    
    return JsonResponse({"error": "Chỉ hỗ trợ POST method"}, status=405)
