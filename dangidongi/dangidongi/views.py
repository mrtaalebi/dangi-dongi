from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import (
    viewsets as rf_viewsets,
    views as rf_views,
    mixins as rf_mixins,
    permissions as rf_permissions,
    status as rf_status,
)

from dangidongi import (
    mixins,
    permissions,
    serializers,
    models,
)


class ProfileViewSet(rf_viewsets.ModelViewSet):

    permission_classes = [
        permissions.CreatesProfile |
        (rf_permissions.IsAuthenticated & permissions.OwnsProfile)
    ]
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()


class ProfilePictureViewSet(rf_viewsets.GenericViewSet, rf_mixins.UpdateModelMixin):

    permission_classes = [
        rf_permissions.IsAuthenticated & permissions.OwnsProfile
    ]
    serializer_class = serializers.ProfilePictureSerializer
    queryset = models.Profile.objects.all()


class LoginViewSet(rf_viewsets.GenericViewSet, rf_mixins.CreateModelMixin):

    serializer_class = serializers.UserLoginSerializer
    queryset = User.objects.all()


class GroupViewSet(rf_viewsets.ModelViewSet):

    permission_classes = [
        rf_permissions.IsAuthenticated,
    ]
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        return self.request.user.profile.groups.all()


class EventViewSet(rf_viewsets.ModelViewSet):

    permission_classes = [
        rf_permissions.IsAuthenticated,
    ]
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        events = self.request.user.profile.events.all()
        shared_with = self.request.query_params.get('shared_with')
        if shared_with is None:
            return events
        shared_with = get_object_or_404(
            models.Profile,
            pk=shared_with
        )
        shared_events = []
        for event in events:
            if shared_with in event.get_people_set():
                shared_events.append(event)
        return self.request.user.profile.events.all()


class PaymentViewSet(rf_viewsets.ModelViewSet):
    permission_classes = [
        rf_permissions.IsAuthenticated,
    ]

    serializer_class = serializers.PaymentSerializer

    def get_queryset(self):
        return models.Payment.objects.filter(payer=self.request.user.profile)
