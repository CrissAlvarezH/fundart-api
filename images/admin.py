from django.contrib import admin

from admin_auto_filters.filters import AutocompleteFilter

from images.models import ImageTag, Image, ImageFavorite


class ImageTagFilter(AutocompleteFilter):
    title = "Tag"
    field_name = "tags"


class ImageAdmin(admin.ModelAdmin):
    list_display = ("preview_mini", "id", "prompt_short", "description_short", "tag_list")
    readonly_fields = ("preview",)
    list_filter = (ImageTagFilter,)
    search_fields = ("prompt", "description")
    search_help_text = "Search by prompt and description"


admin.site.register(Image, ImageAdmin)


class ImageTagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(ImageTag, ImageTagAdmin)


class UserFilter(AutocompleteFilter):
    title = "User"
    field_name = "user"


class ImageFavoriteAdmin(admin.ModelAdmin):
    list_display = ("preview_mini", "user", "image", "created_at")
    list_filter = (UserFilter,)
    autocomplete_fields = ("user", "image")
    readonly_fields = ("preview",)


admin.site.register(ImageFavorite, ImageFavoriteAdmin)
