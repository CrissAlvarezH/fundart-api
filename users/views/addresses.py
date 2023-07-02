from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import Address
from users.serializers import AddressSerializer
from users.permissions import IsSameUser


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated & IsSameUser]

    def get_queryset(self):
        return Address.objects.filter(user_id=self.kwargs.get("user_id"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_id"] = self.kwargs.get("user_id")
        return context

