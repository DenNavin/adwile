from decimal import Decimal

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from django.db import models

from teaser.config import TEASER_PRICE


class AdwileUserManager(UserManager):
    """Менеджер модели User"""

    def replenish_balance_for_teaser(self, user_ids: list) -> None:
        """Пополнение баланса авторов за тизер"""

        for user_id in user_ids:
            user = User.objects.filter(id=user_id).first()
            if user:
                user.replenish_balance(reward=TEASER_PRICE)


class User(AbstractUser):

    balance = models.DecimalField(default=Decimal(0), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    objects = AdwileUserManager()

    def replenish_balance(self, reward: Decimal) -> None:
        """Пополнение баланса автора за тизер"""

        if reward:
            self.balance += reward
            self.save(update_fields=['balance'])
