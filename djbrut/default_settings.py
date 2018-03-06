# coding=utf-8
from .utils import Rule
from . import checkers


CSRF_COOKIE_NAME = 'csrfmiddlewaretoken'

BRUTEFORCE_ERROR = 'Too many requests ({name}). Maximum {limit} per {timelimit} minutes.'
"""
Error message.
Allowed format args:
    * {name} -- checker name.
    * {limit} -- maximum requests for this checker.
    * {timelimit} -- `settings.BRUTEFORCE_TIMELIMIT` value.
"""

BRUTEFORCE_PROTECTION_ENABLED = True
"""
Allow you quick disable all checks.
If BRUTEFORCE_PROTECTION_ENABLED as `False` then `Attempt.check` always return `True`.
"""

BRUTEFORCE_TIMELIMIT = 10  # minutes
"""
Time to live for all attempts counters.
"""

# Rules:
#   * Key: rule name (first arg for `Attempt`)
#   * Value: limits for checkers (namedtuple)
BRUTEFORCE_LIMITS = {
    'default': Rule(
        user=100,       # max requests for one user by BRUTEFORCE_TIMELIMIT
        ip=300,         # max requests for one IP by BRUTEFORCE_TIMELIMIT
        csrf=50,        # max requests with one CSRF token by BRUTEFORCE_TIMELIMIT
        freq=0,         # max request frequency for client [seconds]
    ),
}

# List of checkers for `Attempt`:
BRUTEFORCE_CHECKERS = (
    checkers.CSRFChecker,
    checkers.FrequencyChecker,
    checkers.IPChecker,
    checkers.UserChecker,
)

# Redis settings:
BRUTEFORCE_REDIS_HOST = 'localhost'
BRUTEFORCE_REDIS_PORT = 6379
BRUTEFORCE_REDIS_DB = 0
