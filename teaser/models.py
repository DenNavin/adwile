from django.db import models
from django.utils import timezone

from teaser.config import STATUSES_PAID
from user.models import User


class Teaser(models.Model):

    class Category(models.TextChoices):
        CATEGORY_1 = 'CATEGORY_1', 'Категория 1'
        CATEGORY_2 = 'CATEGORY_2', 'Категория 2'
        CATEGORY_3 = 'CATEGORY_3', 'Категория 3'

    class StatusPaid(models.TextChoices):
        PAID = STATUSES_PAID['paid'], 'Оплачено'
        REJECT = STATUSES_PAID['reject'], 'Отказ'
        UNKNOWN = 'UNKNOWN', 'Неизвестный'

    created_at = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=64)
    description = models.TextField()

    author = models.ForeignKey(User, related_name='teasers', on_delete=models.CASCADE)

    status_paid = models.CharField(max_length=15, choices=StatusPaid.choices, default=StatusPaid.UNKNOWN)
    category = models.CharField(max_length=50, choices=Category.choices)

