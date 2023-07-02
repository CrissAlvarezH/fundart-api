from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import User, City, Department, Address, ConfirmationCode


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'phone', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("full_name", "id", "email", "phone", "is_active")
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone')}),
        ('Permissions', {'fields': ('groups', 'is_staff')}),
        ('Danger zone', {'fields': ('is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'password1', 'password2')}
        ),
    )
    search_fields = ("id", "full_name", "email")
    search_help_text = "Search by id, name or email"
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Department, DepartmentAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "department")
    autocomplete_fields = ("department",)
    list_filter = ("department",)
    search_fields = ("name",)
    search_help_text = "Search by name"


admin.site.register(City, CityAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ("address", "id", "city", "indications", "user")
    autocomplete_fields = ("city", "user")
    search_fields = ("user__id", "user__email", "user__full_name")
    search_help_text = "Search by user id, name or email"


admin.site.register(Address, AddressAdmin)


class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "id", "action", "user")
    autocomplete_fields = ("user",)


admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)
