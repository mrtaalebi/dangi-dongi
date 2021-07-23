from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import serializers

from dangidongi import models


class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password1', 'password2',
        ]
        read_only_fields = [
            'id',
        ]

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
        return User.objects.get(username=username)


class UserLoginSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            self.user = authenticate(
                username=data['username'],
                password=data['password'],
            )
            if self.user is None:
                raise serializers.ValidationError('Unauthorized')
            return data
        except KeyError:
            raise serializers.ValidationError('Unauthorized')

    def create(self, _):
        login(self.context['request'], self.user)
        return self.user


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = models.Profile
        depth = 1
        fields = [
            'user', 'picture', 'card_number',
        ]
        read_only_fields = [
            'picture',
        ]

    def create(serf, validated_data):
        user = UserSerializer(data=validated_data.pop('user'))
        if user.is_valid(raise_exception=True):
            user = user.save()
        validated_data.update({'user': user})
        return models.Profile.objects.create(
            **validated_data
        )


class ProfilePictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = [
            'id', 'picture'
        ]
        read_only_fields = [
            'id',
        ]


class GroupSerializer(serializers.ModelSerializer):

    people_set = serializers.SerializerMethodField()

    def get_people_set(self, group):
        return ProfileSerializer(group.people.all(), many=True).data

    class Meta:
        model = models.Group
        depth = 0
        fields = [
            'id', 'name', 'events', 'people', 'people_set',
        ]
        read_only_fields = [
            'id', 'events', 'people_set',
        ]


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = [
            'latt', 'lang',
        ]


class EventSerializer(serializers.ModelSerializer):

    people_set = serializers.SerializerMethodField()
    where = LocationSerializer()

    def get_people_set(self, event):
        people_set = event.get_people_set()
        return ProfileSerializer(people_set, many=True).data

    class Meta:
        model = models.Event
        depth = 0
        fields = [
            'id', 'title', 'when', 'where', 'description', 'total_cost',
            'payments', 'people', 'people_set',
        ]
        read_only_fields = [
            'id', 'payments', 'people_set',
        ]

    def create(self, validated_data):
        people = validated_data.pop('people')
        where = LocationSerializer(data=validated_data.pop('where'))
        if where.is_valid(raise_exception=True):
            where = where.save()
        event = models.Event.objects.create(
            where=where,
            **validated_data
        )
        for profile in people:
            event.people.add(profile)
        event.people.add(self.context['request'].user.profile)
        return event


class PaymentSerializer(serializers.ModelSerializer):

    payer = ProfileSerializer()
    payee = ProfileSerializer()

    class Meta:
        model = models.Payment
        depth = 0
        fields = [
            'id', 'payer', 'payee', 'amount', 'event', 'is_initial_payment',
            'has_payed', 'pay_proof_image', 'pay_proof_text',
        ]
        read_only_fields = [
            'id',
        ]


