from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import (
    viewsets as rf_viewsets,
    views as rf_views,
    mixins as rf_mixins,
    status as rf_status,
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
    rf_mixins.ListModelMixin,
    rf_mixins.CreateModelMixin,
    rf_mixins.RetrieveModelMixin,
    rf_mixins.UpdateModelMixin,
):

    permission_classes = [
        permissions.PostOrIsAuthenticated
    ]
    serializer_classes = {
        'list': serializers.ProfileSerializer,
        'retrieve': serializers.ProfileSerializer,
        'create': serializers.CreateProfileSerializer,
        'update': serializers.ProfileSerializer,
    }
    queryset = models.Profile.objects.all()


class LoginAPIView(rf_views.APIView):

    def post(self, request):
        try:
            user = authenticate(
                username=request.data['username'],
                password=request.data['password'],
            )
            if user is None:
                return Response(
                    status=rf_status.HTTP_401_UNAUTHORIZED
                )
            login(request, user)
            return Response(
                status=rf_status.HTTP_202_ACCEPTED
            )
        except KeyError:
            return Response(
                status=rf_status.HTTP_400_BAD_REQUEST
            )


class GroupViewSet(
    # mixins.MultiSerializerMixin,
    rf_viewsets.GenericViewSet,
    rf_mixins.CreateModelMixin,
    rf_mixins.RetrieveModelMixin,
    rf_mixins.UpdateModelMixin,
):

    permission_classes = [
        # rf_permissions.IsAuthenticated
    ]
    # serializer_classes = {
    #     'create': serializers.CreateProfileSerializer,
    #     'retrieve': serializers.ProfileSerializer,
    #     'update': serializers.ProfileSerializer,
    # }
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
