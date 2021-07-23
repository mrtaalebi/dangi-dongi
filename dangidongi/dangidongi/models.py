import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Payment(models.Model):
    payer = models.ForeignKey(
        User,
        related_name='payer_payments',
        on_delete=models.CASCADE
    )
    payee = models.ForeignKey(
        User,
        related_name='payee_payments',
        on_delete=models.CASCADE,
        null=True
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
    )
    pay_proof_text = models.TextField()


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
    payments = models.ForeignKey(
        Payment,
        related_name='events',
        on_delete=models.CASCADE
    )


class Group(models.Model):
    name = models.CharField(
        max_length=100,
    )
    events = models.ManyToManyField(
        Event,
        related_name='groups'
    )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
    def name_it(_, __):
        return uuid.uuid4().hex + '.jpg'
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
    groups = models.ManyToManyField(
        Group,
        related_name='people'
    )
    events = models.ManyToManyField(
        Event,
        related_name='people'
    )

