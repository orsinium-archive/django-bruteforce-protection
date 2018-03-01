# coding=utf-8
from .utils import Rule
from . import checkers


CSRF_COOKIE_NAME = 'csrfmiddlewaretoken'

BRUTEFORCE_ERROR = 'Too many requests'

BRUTEFORCE_PROTECTION_ENABLED = True
BRUTEFORCE_TIMELIMIT = 10  # minutes
BRUTEFORCE_LIMITS = {
    'default': Rule(
        user=100,       # max requests for one user by TIMELIMIT
        ip=300,         # max requests for one IP by TIMELIMIT
        csrf=50,        # max requests with one CSRF token by TIMELIMIT
        freq=0,         # max request frequency for client [seconds]
    ),
}

BRUTEFORCE_CHECKERS = (
    checkers.CSRFChecker,
    checkers.FrequencyChecker,
    checkers.IPChecker,
    checkers.UserChecker,
)

BRUTEFORCE_REDIS_HOST = 'localhost'
BRUTEFORCE_REDIS_PORT = 6379
BRUTEFORCE_REDIS_DB = 0
