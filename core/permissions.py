from rest_framework import exceptions, permissions

DONT_HAVE_ADMIN_PERMISSION = "You Don't Have Administrations Permission"

# Checks Whether User Admin User
class IsAdministerUser(permissions.BasePermission):
    message = DONT_HAVE_ADMIN_PERMISSION

    def has_permission(self, request, view):
        return request.user.is_admin
