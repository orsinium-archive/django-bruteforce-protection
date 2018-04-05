# DjBrut

![DjBrut logo](logo.png)

[![Build Status](https://travis-ci.org/orsinium/django-bruteforce-protection.svg?branch=master)](https://travis-ci.org/orsinium/django-bruteforce-protection) [![PyPI version](https://img.shields.io/pypi/v/djbrut.svg)](https://pypi.python.org/pypi/djbrut) [![Status](https://img.shields.io/pypi/status/djbrut.svg)](https://pypi.python.org/pypi/djbrut) [![Code size](https://img.shields.io/github/languages/code-size/orsinium/django-bruteforce-protection.svg)](https://github.com/orsinium/django-bruteforce-protection) [![License](https://img.shields.io/pypi/l/djbrut.svg)](LICENSE)

DjBrut -- simple brutforce protection for Django project.

Default checkers:

* Max requests for IP.
* Max requests for user.
* Max requests for one CSRF-token (stupid but effective).
* Max requests frequency limitation.

DjBrut use Redis as storage for all counters.

## Installation

```
pip install djbrut
```

## Usage

```python
from django.http import HttpResponse
from djbrut import Attempt

def some_view(request):
    attempt = Attempt('some rule type name', request)
    # check
    if not attempt.check():
        # error
        return HttpResponse(attempt.error)
    # success
    ...
```

You can see [example project](example/) for more details.

## Configuring

Just set up rules:

```python
BRUTEFORCE_LIMITS = {
    'default': Rule(
        user=100,       # max requests for one user by BRUTEFORCE_TIMELIMIT
        ip=300,         # max requests for one IP by BRUTEFORCE_TIMELIMIT
        csrf=50,        # max requests with one CSRF token by BRUTEFORCE_TIMELIMIT
        freq=0,         # max request frequency for client [seconds]
    ),
    'some rule type name': Rule(
        user=100,       # max requests for one user by BRUTEFORCE_TIMELIMIT
        ip=300,         # max requests for one IP by BRUTEFORCE_TIMELIMIT
        csrf=50,        # max requests with one CSRF token by BRUTEFORCE_TIMELIMIT
        freq=0,         # max request frequency for client [seconds]
    ),
}
```

`Attempt` get rule type name as first arg. If rule type name not found in keys of BRUTEFORCE_LIMITS, 'default' will be used. If you don't set default rule then passed rule type must be exists in BRUTEFORCE_LIMITS keys.

`BRUTEFORCE_TIMELIMIT` -- time to live for all attempts counters.

You can see [default settings](djbrut/default_settings.py) for more params such as custom error message.
