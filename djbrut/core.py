# -*- coding: utf-8 -*-
import redis
from .settings import settings

for checker in settings.BRUTEFORCE_CHECKERS:
    checker.settings = settings


class Attempt(object):
    """Check request by all possible checkers for specified rule type
    """
    error = None
    connection = redis.StrictRedis(
        host=settings.BRUTEFORCE_REDIS_HOST,
        port=settings.BRUTEFORCE_REDIS_PORT,
        db=settings.BRUTEFORCE_REDIS_DB,
    )

    def __init__(self, rule_type, request, **kwargs):
        self.checkers = []
        for checker in settings.BRUTEFORCE_CHECKERS:
            checker = checker(self.connection, request, rule_type, **kwargs)
            self.checkers.append(checker)

    def incr(self):
        """Increment counters for all checkers
        """
        for checker in self.checkers:
            checker.incr()

    def check(self, incr=True):
        """Check request by all checkers
        Return True if all is fine, False otherwise.
        """
        if not settings.BRUTEFORCE_PROTECTION_ENABLED:
            return True
        for checker in self.checkers:
            if not checker.check():
                self.error = checker.get_error()
                return False
        if incr:
            self.incr()
        return True
