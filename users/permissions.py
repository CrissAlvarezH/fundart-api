from rest_framework.permissions import BasePermission


class IsSameUser(BasePermission):
    message = "you are not the correct user"

    def has_permission(self, request, view):
        return str(request.user.id) == view.kwargs.get("user_id")
