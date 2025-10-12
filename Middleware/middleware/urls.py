from django.urls import path
from .views import jwt_login, refresh_token_view

urlpatterns = [
    path("jwt-login/", jwt_login, name="jwt_login"),
    path("refresh-token/", refresh_token_view, name="refresh_token"),
]
