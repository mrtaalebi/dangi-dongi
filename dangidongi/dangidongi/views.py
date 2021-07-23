from rest_framework import (
    viewsets as rf_viewsets,
    mixins as rf_mixins,
)

from dangidongi import (
    mixins,
    permissions,
    serializers,
    models,
)

class ProfileViewSet(
    mixins.MultiSerializerMixin,
    rf_viewsets.GenericViewSet,
    rf_mixins.CreateModelMixin,
    rf_mixins.RetrieveModelMixin,
    rf_mixins.UpdateModelMixin,
):

    permission_classes = [
        permissions.PostOrIsAuthenticated
    ]
    serializer_classes = {
        'create': serializers.CreateProfileSerializer,
        'retrieve': serializers.ProfileSerializer,
        'update': serializers.ProfileSerializer,
    }
    queryset = models.Profile.objects.all()

