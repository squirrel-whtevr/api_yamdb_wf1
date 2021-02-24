from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_admin
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_moderator
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in
                permissions.SAFE_METHODS
                or (not request.user.is_anonymous
                    and request.user.is_admin))


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (not request.user.is_anonymous
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method in
                permissions.SAFE_METHODS
                or request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user)
