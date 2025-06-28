from rest_framework import permissions


class IsEmpresaOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.empresa.empresa_usuarios.filter(user=request.user).exists()