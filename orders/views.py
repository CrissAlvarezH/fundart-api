from rest_framework import viewsets, mixins

from orders.models import Order, OrderStatusHistory, OrderPhoneCase, Coupon
from orders.serializers import OrderSerializer, OrderCreateSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return OrderSerializer
        elif self.action == "create":
            return OrderCreateSerializer
        raise NotImplementedError("serializer not implemented")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_id"] = self.request.user.id
        return context
