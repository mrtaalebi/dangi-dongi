from rest_framework import permissions


class CreatesProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'


class OwnsProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user.profile

