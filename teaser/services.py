from django.db import transaction

from teaser.models import Teaser
from user.models import User


@transaction.atomic
def change_teaser_status(teaser_ids: list, status_paid: 'str') -> list:
    """Обновление статуса тизеров, только для тизеров со статусом UNKNOWN"""

    teasers = Teaser.objects.filter(id__in=teaser_ids, status_paid=Teaser.StatusPaid.UNKNOWN)

    author_ids = []
    data = []
    for t in teasers:
        author_ids.append(t.author_id)
        data.append({'id': t.id, 'title': t.title})

    User.objects.replenish_balance_for_teaser(user_ids=[x.author_id for x in teasers])
    teasers.update(status_paid=status_paid)

    return data




