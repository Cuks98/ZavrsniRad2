from rest_framework import permissions

class IsRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role_id == 1
    
class IsRoleUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role_id == 2 or user.role_id == 1)
    
class IsRoleMember(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role_id == 2 or user.role_id == 1 or user.role_id == 3)
