from django.contrib.auth.models import User
from rest_framework import serializers

from dangidongi import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
        ]


class PaymentSerializer(serializers.ModelSerializer):

    payer = UserSerializer()
    payee = UserSerializer()
    pay_proof_image = serializers.ImageField()

    class Meta:
        model = models.Payment
        fields = [
            'id', 'payer', 'payee', 'amount', 'is_initial_payment',
            'has_payed', 'pay_proof_image', 'pay_proof_text',
        ]


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = [
            'latt',
            'lang',
        ]


class EventSerializer(serializers.ModelSerializer):

    payments = PaymentSerializer(many=True)
    where = LocationSerializer()

    class Meta:
        model = models.Event
        fields = [
            'id', 'title', 'when', 'where', 'description', 'total_cost',
            'payments',
        ]


class GroupSerializer(serializers.ModelSerializer):

    events = EventSerializer(many=True)

    class Meta:
        model = models.Group
        fields = [
            'id', 'events'
        ]


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    groups = GroupSerializer(many=True)
    events = EventSerializer(many=True)

    class Meta:
        model = models.Profile
        fields = [
            'user',
            'picture',
            'card_number',
            'groups',
            'events',
        ]
        read_only_fields = [
            'groups',
            'events',
        ]


class CreateProfileSerializer(serializers.Serializer):

    username = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    card_number = serializers.CharField(write_only=True)
    picture = serializers.FileField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords mismatch')
        return data

    def create(self, validated_data):
        username = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password1'],
        )
        user = User.objects.get(username=username)
        profile = models.Profile.objects.create(
            user=user,
            picture=validated_data['picture'],
            card_number=validated_data['card_number'],
        )
        return profile

