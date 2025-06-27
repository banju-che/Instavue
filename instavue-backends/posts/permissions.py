from rest_framework import permissions


class IsPostOwnerOrAdminMod(permissions.BasePermission):
    """
    Allow post owners to edit/delete. Admins and moderators can also modify.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.user == request.user:
            return True

        return request.user.role in ['admin', 'moderator']
