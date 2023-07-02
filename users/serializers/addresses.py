from rest_framework import serializers

from users.models import Address, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id", "city", "address", "indications",
            "receiver_name", "receiver_phone"
        )

    def to_representation(self, instance):
        return {
            **super().to_representation(instance),
            "city": CitySerializer(instance.city).data,
            "user": instance.user.id,
        }

    def create(self, validated_data):
        validated_data["user_id"] = self.context.get("user_id")
        return super().create(validated_data)
