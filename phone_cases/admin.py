from django.contrib import admin

from admin_auto_filters.filters import AutocompleteFilter

from phone_cases.models import (
    PhoneCase, Discount, PhoneBrand, PhoneBrandReference, CaseType, CaseTypeImage
)


class BrandRefFilter(AutocompleteFilter):
    title = "Brand Ref"
    field_name = "phone_brand_ref"


class CaseTypeFilter(AutocompleteFilter):
    title = "Case type"
    field_name = "case_type"


class DiscountFilter(AutocompleteFilter):
    title = "Discount"
    field_name = "discount"


class PhoneCaseAdmin(admin.ModelAdmin):
    list_display = (
        "phone_brand_ref", "id", "price", "sale_price", "inventory_status", "case_type",
        "discount", "is_active",
    )
    list_filter = (BrandRefFilter, CaseTypeFilter, DiscountFilter, "inventory_status", "is_active")
    autocomplete_fields = ("phone_brand_ref", "case_type", "discount")
    readonly_fields = ("scaffold_preview",)
    search_fields = ("phone_brand_ref__name",)
    search_help_text = "Filter by brand ref name"


admin.site.register(PhoneCase, PhoneCaseAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "rate", "valid_until")
    search_fields = ("name", "rate")
    search_help_text = "Search by name and rate"


admin.site.register(Discount, DiscountAdmin)


class PhoneBrandAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(PhoneBrand, PhoneBrandAdmin)


class PhoneBrandReferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "brand")
    list_filter = ("brand",)
    search_fields = ("name", "brand__name")
    search_help_text = "Search by name and brand name"
    autocomplete_fields = ("brand",)


admin.site.register(PhoneBrandReference, PhoneBrandReferenceAdmin)


class CaseTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_preview_mini")
    search_fields = ("name",)
    search_help_text = "Search by name"
    readonly_fields = ("icon_preview",)


admin.site.register(CaseType, CaseTypeAdmin)


class CaseTypeImageAdmin(admin.ModelAdmin):
    list_display = ("img_preview_mini", "id", "order_priority", "case_type")
    autocomplete_fields = ("case_type", )
    list_filter = ("case_type",)
    search_fields = ("case_type__name",)
    search_help_text = "Search by case type name"
    readonly_fields = ("img_preview",)


admin.site.register(CaseTypeImage, CaseTypeImageAdmin)
