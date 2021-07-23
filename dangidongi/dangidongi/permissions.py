from rest_framework import permissions


class PostOrIsAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(permissions.IsAuthenticated, self).has_permission(
            request, view
        )
