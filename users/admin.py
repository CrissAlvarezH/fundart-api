from django.contrib import admin

from users.models import User, City, Department, Address


class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "id", "email", "phone", "is_active")
    search_fields = ("id", "full_name", "email")
    search_help_text = "Search by id, name or email"


admin.site.register(User, UserAdmin)

admin.site.register(Department)


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "department")
    list_filter = ("department",)
    search_fields = ("name",)
    search_help_text = "Search by name"


admin.site.register(City, CityAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ("address", "id", "department", "city", "indications", "user")
    search_fields = ("user__id", "user__email", "user__full_name")
    search_help_text = "Search by user id, name or email"


admin.site.register(Address, AddressAdmin)

