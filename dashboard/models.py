from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from localflavor.generic.models import IBANField
from djmoney.models.fields import MoneyField

# Constants
ENVIRONMENT_CHOICES = [
        ('SANDBOX', 'SANDBOX'),
        ('PRODUCTION', 'PRODUCTION')
    ]
MONETARY_ACCOUNT_TYPES = [
        ('MB', 'MonetaryAccountBank'),
        ('MJ', 'MonetaryAccountJoint'),
        ('MS', 'MonetaryAccountSavings'),
    ]

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bunq_api_key = models.CharField(max_length=64, blank=True)
    bunq_api_environment = models.CharField(max_length=10, choices=ENVIRONMENT_CHOICES, blank=True)


class MonetaryAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monetary_account_id = models.IntegerField(unique=True)
    monetary_account_type = models.CharField(max_length=2, choices=MONETARY_ACCOUNT_TYPES)
    iban = IBANField(unique=True)
    display_name = models.CharField(max_length=128, blank=True)
    description = models.TextField()
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    savings_goal = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='EUR',
        blank=True,
        null=True
    )
    savings_goal_progress = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=128)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    instance.settings.save()
