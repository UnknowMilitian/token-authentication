from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "title", "description"]


# Registration section of serializers
class UserLoginSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True, style={"input_type": "password"})
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["user_id", "username", "password"]


class UserRegisterSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(style={"input_type": "password"})
    email = serializers.EmailField(style={"input_type": "password"})
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {"detail": "User already exists!"}
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        # Проверяем совпадение паролей
        if instance["password"] != instance["password2"]:
            raise ValidationError({"message": "Both passwords must match"})

        # Проверяем, существует ли email
        if User.objects.filter(email=instance["email"]).exists():
            raise ValidationError({"message": "Email already exists!"})

        # Обязательно возвращаем валидированные данные
        return instance

    def create(self, validated_data):
        password = validated_data.pop("password")
        password2 = validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
