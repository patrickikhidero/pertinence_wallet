from django.db import models
from transactions.models import Wallet


class InformationForTransaction(models.Model):
    currency_types = (
        ('EUR', 'EUR'),
        ('CHF', 'CHF'),
        ('USD', 'USD'),
    )

    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, related_name="information", verbose_name='Information'
    )
    last_used_currency = models.CharField(choices=currency_types, default='EUR', max_length=3)

    def __str__(self):
        return f"Currency used for requests is {self.last_used_currency} "