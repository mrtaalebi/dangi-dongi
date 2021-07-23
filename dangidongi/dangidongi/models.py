import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
    def name_it(_, filename):
        return uuid.uuid4().hex + '.' + filename.split('.')[-1]
    picture = models.ImageField(
        max_length=200,
        upload_to=name_it,
    )
    card_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex='^(\d{16})|(\d{20})$',
                message='Invalid card number',
            )
        ],
    )


class Group(models.Model):
    name = models.CharField(
        max_length=100,
    )
    people = models.ManyToManyField(
        Profile,
        related_name='groups'
    )


class Location(models.Model):
    latt = models.FloatField()
    lang = models.FloatField()


class Event(models.Model):
    title = models.CharField(
        max_length=200
    )
    when = models.DateTimeField()
    where = models.ForeignKey(
        Location,
        related_name='event',
        on_delete=models.CASCADE,
        null=True
    )
    description = models.TextField()
    total_cost = models.FloatField(
        validators=[
            RegexValidator(
                regex='\d+([.]\d*)?',
                message='Total cost must be positive',
            )
        ],
    )
    people = models.ManyToManyField(
        Profile,
        related_name='events'
    )
    groups = models.ManyToManyField(
        Group,
        related_name='events'
    )

    def get_people_set(self):
        people_set = set(self.people.all())
        for group in self.groups.all():
            for profile in group.people.all():
                people_set.append(profile)
        return people_set


class Payment(models.Model):
    payer = models.ForeignKey(
        Profile,
        related_name='payer_payments',
        on_delete=models.CASCADE
    )
    payee = models.ForeignKey(
        Profile,
        related_name='payee_payments',
        on_delete=models.CASCADE,
        null=True
    )
    event = models.ForeignKey(
        Event,
        related_name='payments',
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        validators=[
            RegexValidator(
                regex='\d+([.]\d*)?',
                message='Payment amount must be positive',
            )
        ],
    )
    is_initial_payment = models.BooleanField()
    has_payed = models.BooleanField()
    pay_proof_image = models.ImageField(
        max_length=200,
        null=True
    )
    pay_proof_text = models.TextField(
        null=True
    )


