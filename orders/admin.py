from django.contrib import admin

from admin_auto_filters.filters import AutocompleteFilter

from orders.models import Order, OrderStatusHistory, OrderPhoneCase, Coupon


class UserFilter(AutocompleteFilter):
    title = "User"
    field_name = "user"


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user", "id", "total", "created_at", "current_status", "address",
        "coupons_resume",
    )
    list_filter = (UserFilter,)
    search_fields = ("id", "user__email")
    search_help_text = "Search by id and user email"


admin.site.register(Order, OrderAdmin)


class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("order", "id", "status", "set_at", "details", "user")
    search_fields = ("status", "details")
    search_help_text = "Search by status and details"


admin.site.register(OrderStatusHistory, OrderStatusHistoryAdmin)


class OrderPhoneCaseAdmin(admin.ModelAdmin):
    list_display = ("order", "id", "phone_case", "quantity", "price", "discount")


admin.site.register(OrderPhoneCase, OrderPhoneCaseAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "value", "discount_rate", "is_free_shipping", "uses", "max_uses",
        "for_all_phone_cases", "is_valid", "valid_until", "created_at",
    )
    readonly_fields = ("is_valid",)


admin.site.register(Coupon, CouponAdmin)
