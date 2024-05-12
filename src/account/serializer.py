from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
