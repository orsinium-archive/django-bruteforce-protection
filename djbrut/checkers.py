

class BaseChecker(object):
    """Base class for checkers
    In common case you want redefine in child only two attributes:
        * `name` attribute
        * `get_value` method
    """
    key = None  # key for Redis
    key_template = '{rule}:{checker}:{value}:int'  # template for key

    settings = NotImplemented   # Django settings
    name = NotImplemented       # checker name

    def __init__(self, connection, request, rule_type, **kwargs):
        self.connection = connection                    # for get_attempts and incr
        self.request = request                          # for logging
        self.limit = self.get_limit(rule_type)          # for check
        self.key = self.get_key(request, rule_type, **kwargs)   # for redis connection

    def get_key(self, request, rule_type, **kwargs):
        """Generate key for Redis
        """
        value = self.get_value(request, **kwargs)
        if value is None:
            return
        return self.key_template.format(
            rule=rule_type,
            checker=self.name,
            value=value
        )

    def get_value(self, request):
        """Get key parameter for Redis key.
        IP-address, client id etc.
        """
        raise NotImplementedError

    def get_limit(self, rule_type):
        """Git limit from rule for current check
        """
        if rule_type in self.settings.BRUTEFORCE_LIMITS:
            rule = self.settings.BRUTEFORCE_LIMITS[rule_type]
        else:
            rule = self.settings.BRUTEFORCE_LIMITS['default']
        return getattr(rule, self.name)

    def incr(self):
        """Increment attempts count
        """
        if not self.key:
            return
        if self.connection.exists(self.key):
            self.connection.incr(self.key, 1)
        else:
            self.connection.set(self.key, 1)
            self.connection.expire(self.key, self.settings.BRUTEFORCE_TIMELIMIT * 60)

    def get_attempts(self):
        """Get current attempts count
        """
        if not self.key:
            return 0
        data = self.connection.get(self.key)
        if not data:
            return 0
        return int(data)

    def log(self):
        """Log limit activation
        """
        # TODO: add logging
        pass

    def get_error(self):
        """Generate error message
        """
        key = 'BRUTEFORCE_ERROR_{}'.format(self.name)
        template = getattr(self.settings, key, self.settings.BRUTEFORCE_ERROR)
        return template.format(
            name=self.name,
            limit=self.limit,
        )

    def check(self):
        """Check. Just check.
        Return True if all is fine, False otherwise.
        """
        # if disabled
        if not self.key:
            return True
        if not self.limit:
            return True
        # get attempts
        count = self.get_attempts()
        # if first activation
        if count == self.limit:
            self.log()
        # compare with limit
        return count < self.limit


class UserChecker(BaseChecker):
    name = 'user'

    def get_value(self, request, user=None, **kwargs):
        if not user:
            if not request:
                return
            if not getattr(request, 'user'):
                return
            if not getattr(request, 'user'):
                return
            user = request.user
        if not user.is_authenticated():
            return
        return user.pk


class IPChecker(BaseChecker):
    name = 'ip'

    def get_value(self, request, **kwargs):
        if not request:
            return
        return request.META['REMOTE_ADDR']


class CSRFChecker(BaseChecker):
    name = 'csrf'

    def get_value(self, request, **kwargs):
        if not request:
            return
        return getattr(request.POST, self.settings.CSRF_COOKIE_NAME, None)


class FrequencyChecker(UserChecker):
    name = 'freq'

    def log(self):
        pass

    def incr(self):
        if not self.key:
            return
        if not self.limit:
            return
        self.connection.set(self.key, 0)
        self.connection.expire(self.key, self.limit)

    def check(self):
        if not self.key:
            return True
        if not self.limit:
            return True
        if not self.connection.exists(self.key):
            return True
        ttl = self.connection.ttl(self.key_freq)
        if ttl >= 0:
            return True
        self.log()
        return False
