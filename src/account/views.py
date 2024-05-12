from importlib import import_module
from django.contrib.auth import login, logout, authenticate
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from .serializer import LoginSerializer


class AuthViewSet(viewsets.ViewSet):
    # 自動ではOpenAPIに引数が正しく書き出されない。

    def get_permissions(self):
        if self.action == "login":
            return []

        return [permissions.IsAuthenticated()]

    @action(methods=["post"], detail=False)
    def login(self, request, *args, **kwargs):
        logout(request)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)
        if user is None or not user.is_active:
            raise serializers.ValidationError("User isn't exist.")
        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenViewSet(
    viewsets.ViewSet,
):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        token, _ = Token.objects.update_or_create(user=request.user)
        print(token)
        return Response({"token": token.key, "created": token.created})

    @action(methods=["delete"], detail=False)
    def delete(self, request, *args, **kwargs):
        token, _ = Token.objects.get_or_create(user=request.user)
        token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
