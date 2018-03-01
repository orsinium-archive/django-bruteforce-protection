# -*- coding: utf-8 -*-
import redis
from .settings import settings


# types
TYPE_IP = 'ip'
TYPE_CLIENT = 'client'
TYPE_CSRF = 'csrf'


class Attempt(object):
    error = None

    connection = redis.StrictRedis(
        host=settings.BRUTEFORCE_REDIS_HOST,
        port=settings.BRUTEFORCE_REDIS_PORT,
        db=settings.BRUTEFORCE_REDIS_DB,
    )

    def __init__(self, rule_type, request):
        self.checkers = []
        for checker in settings.BRUTEFORCE_CHECKERS:
            self.checkers.append(checker(self.connection, request, rule_type))

    def incr(self):
        for checker in self.checkers:
            checker.incr()

    def is_ok(self, incr=True):
        if not settings.BRUTEFORCE_PROTECTION_ENABLED:
            return True
        for checker in self.checkers:
            if not checker.check():
                self.error = self.get_error()
                return False
        return True
