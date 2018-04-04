# coding=utf-8
from django.test import TestCase, Client, RequestFactory
from djbrut import Attempt, clear


class DjBrutTest(TestCase):
    def setUp(self):
        clear()

    def test_view(self):
        client = Client()

        # first 5 requests is ok
        for _i in range(5):
            response = client.get('/')
            self.assertEqual(response.content, b'ok')

        # 6st requests is failed
        response = client.get('/')
        self.assertEqual(response.content, b'Too many requests (ip). Maximum 5 per 1 minutes.')

    def test_timelimit(self):
        factory = RequestFactory()
        request = factory.get('/')
        attempt = Attempt('index', request)
        attempt.check()
        for key in attempt.connection.keys('*:ip:*:int'):
            self.assertLessEqual(attempt.connection.ttl(key), 60)

    def test_check(self):
        factory = RequestFactory()
        request = factory.get('/')
        for _i in range(5):
            attempt = Attempt('index', request)
            self.assertTrue(attempt.check())
        attempt = Attempt('index', request)
        self.assertFalse(attempt.check())

    def test_default_rule(self):
        factory = RequestFactory()
        request = factory.get('/')
        for _i in range(10):
            attempt = Attempt('lorem ipsum', request)
            self.assertTrue(attempt.check())
        attempt = Attempt('lorem ipsum', request)
        self.assertFalse(attempt.check())
