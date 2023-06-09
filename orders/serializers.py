from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import UserSerializer
from users.serializers import AddressSerializer
from phone_cases.serializers import PhoneCaseSerializer, DiscountSerializer
from images.serializers import ImageSerializer

from orders.models import Order, OrderPhoneCase, Coupon
from users.models import Address


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class OrderPhoneCaseSerializer(serializers.ModelSerializer):
    phone_case = PhoneCaseSerializer()
    discount = DiscountSerializer()
    image = ImageSerializer()

    class Meta:
        model = OrderPhoneCase
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()
    cases = OrderPhoneCaseSerializer(source="orderphonecase_set", many=True)
    coupons = CouponSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id", "current_status", "total", "user", "address", "cases",
            "coupons", "created_at",
        )


class OrderPhoneCaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPhoneCase
        fields = ("phone_case", "quantity", "image")


class OrderCreateSerializer(serializers.Serializer):
    address = serializers.IntegerField()
    coupons = serializers.ListSerializer(child=serializers.CharField())
    phone_cases = OrderPhoneCaseCreateSerializer(many=True)

    def to_representation(self, instance):
        return OrderSerializer(instance).data

    def validate_address(self, address):
        if not Address.objects.filter(id=address).exists():
            return ValidationError("address does not exists")
        return address

    def validate_coupons(self, coupons):
        for c in coupons:
            coupon = Coupon.objects.filter(value=c).first()
            if not coupon:
                raise ValidationError(f"coupon '{c}' does not exists")
            if timezone.now() > coupon.valid_until:
                raise ValidationError(f"coupon '{c}' expired")
        return coupons

    def validate_phone_cases(self, phone_cases):
        if len(phone_cases) == 0:
            raise ValidationError("must have phone cases")
        return phone_cases

    def validate(self, data):
        # validate if this coupon is for the case in the order
        case_ids = [str(pc["phone_case"]) for pc in data["phone_cases"]]
        for c in data.get("coupons", []):
            coupon = Coupon.objects.filter(value=c).first()
            if coupon.for_all_phone_cases:
                continue

            coupon_case_ids = [str(pc.id) for pc in coupon.phone_cases.all()]

            # if all the cases in order are allowed to use with this coupon
            if set(case_ids).intersection(set(coupon_case_ids)) != set(case_ids):
                raise ValidationError(f"coupon '{c}' is not allowed to theses cases")
        return data

    def create(self, validated_data):
        for c in validated_data.get("coupons"):
            was_used = Coupon.objects.get(value=c).use()
            if not was_used:
                raise ValidationError(f"coupon '{c}' was already used")

        order = Order.objects.create(
            user_id=self.context.get("user_id"),
            address_id=validated_data.get("address"),
        )

        order.coupons.add(*validated_data.get("coupons"))
        for pc in validated_data.get("phone_cases"):
            OrderPhoneCase.objects.create(
                order=order,
                discount=pc["phone_case"].discount,
                price=pc["phone_case"].price,
                **pc,
            )
        return order