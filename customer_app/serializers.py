from rest_framework import serializers
from customer_app.models import Customer as User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "phone_number",
            "token",
        ]
        read_only_fields = [
            "id",
            "phone_number",
            "token",
            "username",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "is_active",
        )


class UserSerializerrrrr(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "created_at",
            "updated_at",
        ]
