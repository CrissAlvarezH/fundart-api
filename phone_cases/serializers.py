from rest_framework import serializers

from phone_cases.models import PhoneCase, Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class PhoneCaseSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer()

    class Meta:
        model = PhoneCase
        fields = (
            "id", "price", "sale_price", "discount",
            "inventory_status", "phone_brand_ref", "case_type",
            "case_scaffold_img", "is_active",
        )
