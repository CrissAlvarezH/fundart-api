from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from users.services import user_create


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "full_name", "email", "phone", "group_names")
        model = User


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(min_length=6)

    class Meta:
        fields = ("full_name", "email", "phone", "password")
        model = User

    def create(self, validated_data):
        return user_create(**validated_data)

