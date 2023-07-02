from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

from users.models import User, ConfirmationCode
from users.serializers import UserSerializer, UserSignUpSerializer
from users.services import (
    send_email_verification_code, create_verification_account_code,
    change_user_password
)


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["GET"])
    def me(self, request):
        return Response(data=UserSerializer(request.user).data)

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=UserSerializer(user).data)


class UserPasswordViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["POST"], url_path="request-recovery")
    def request_recovery(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()
        if user is None:
            raise ValidationError("email does not exists")

        code = create_verification_account_code(user)
        send_email_verification_code(user, code)

        return Response({"details": "email sent successfully"})

    @action(detail=False, methods=["POST"])
    def recovery(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        code = request.data.get("code")

        user = User.objects.filter(email=email).first()
        if user is None:
            raise ValidationError("invalid data")

        confirmation_code = ConfirmationCode.objects.filter(code=code, user=user).first()
        if confirmation_code is None:
            raise ValidationError("invalid data")

        if len(new_password) < 6:
            raise ValidationError("password length must be bigger than 6")

        change_user_password(user, new_password)

        return Response({"details": "password changed"})
