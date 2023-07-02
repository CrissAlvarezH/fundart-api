from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user"] = {
            "id": user.id,
            "full_name": user.full_name,
            "group_names": user.group_names
        }

        return token
