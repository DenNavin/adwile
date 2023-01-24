import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adwile.settings")
django.setup()

from django.test import TestCase

from rest_framework.test import APIClient

from teaser.models import Teaser
from user.models import User


class TestCaseTeaser(TestCase):

    author_username = 'test'
    admin_username = 'admin'
    teaser_title = 'teaser'
    url = 'http://127.0.0.1:8000/api/teaser_status/'

    def setUp(self):
        self.client = APIClient()

        user = User.objects.create(username=self.author_username)
        Teaser.objects.create(title=self.teaser_title, description='test', category=Teaser.Category.CATEGORY_1, author=user)

    def test_author_change_teaser_status(self):
        """Смена статуса тизера автором"""

        user = User.objects.get(username=self.author_username)
        teaser = Teaser.objects.get(title=self.teaser_title)

        data = {"teaser_ids": [teaser.id], "status_paid": Teaser.StatusPaid.PAID}
        self.client.force_authenticate(user)
        response = self.client.put(path=self.url, data=data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
        self.assertEqual(teaser.status_paid, Teaser.StatusPaid.UNKNOWN)

    def test_admin_change_teaser_status_paid(self):
        """Смена статуса тизера админом на PAID"""

        user = User.objects.first()
        teaser = Teaser.objects.get(title=self.teaser_title)

        data = {"teaser_ids": [teaser.id], "status_paid": Teaser.StatusPaid.PAID}
        self.client.force_authenticate(user)
        response = self.client.put(path=self.url, data=data)

        teaser.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(teaser.status_paid, Teaser.StatusPaid.PAID)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['teaser_data'][0]['id'], teaser.id)

    def test_admin_change_teaser_status_reject(self):
        """Смена статуса тизера админом на REJECT"""

        user = User.objects.first()
        teaser = Teaser.objects.get(title=self.teaser_title)

        data = {"teaser_ids": [teaser.id], "status_paid": Teaser.StatusPaid.REJECT}
        self.client.force_authenticate(user)
        response = self.client.put(path=self.url, data=data)

        teaser.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(teaser.status_paid, Teaser.StatusPaid.REJECT)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['teaser_data'][0]['id'], teaser.id)

    def test_admin_change_paid_teaser_status(self):
        """Смена статуса тизера админом на REJECT, когда статус тизера уже установлен"""

        user = User.objects.first()
        teaser = Teaser.objects.get(title=self.teaser_title)

        data = {"teaser_ids": [teaser.id], "status_paid": Teaser.StatusPaid.REJECT}
        self.client.force_authenticate(user)
        self.client.put(path=self.url, data=data)
        data['status_paid'] = Teaser.StatusPaid.PAID
        response = self.client.put(path=self.url, data=data)

        teaser.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(teaser.status_paid, Teaser.StatusPaid.REJECT)

