# coding=utf-8
from django.test import TestCase, Client
from djbrut import Attempt, clear


class DjBrutTest(TestCase):
    def setUp(self):
        clear()

    def test_view(self):
        """Test view
        """
        client = Client()

        # first 5 requests is ok
        for _i in range(5):
            response = client.get('/')
            self.assertEqual(response.content, b'ok')

        # 6st requests is failed
        response = client.get('/')
        self.assertEqual(response.content, b'Too many requests (ip). Maximum 5 per 1 minutes.')
