from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):  # Прописываем проверку прав доступа для владельца и менеджера(is_staff)
    def has_object_permission(self, request, view, object):
        return request.user == object.owner


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()


class IsSuperuser(BasePermission):
    def has_object_permission(self, request, view, object):
        if request.user.is_superuser:
            return True

        return False
