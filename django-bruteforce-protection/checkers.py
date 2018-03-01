

class BaseChecker(object):
    key = None
    error = None
    key_template = '{rule}:{checker}:{value}:int'

    settings = NotImplemented
    name = NotImplemented

    def __init__(self, connection, request, rule_type):
        self.connection = connection            # for get_attempts
        self.request = request                  # for logging
        self.limit = self.get_limit(rule_type)
        self.key = self.get_key(request, rule_type)

    def get_key(self, request, rule_type):
        value = self.get_value(request)
        if value is None:
            return
        return self.key_template.format(
            rule=rule_type,
            checker=self.name,
            value=value
        )

    def get_value(self, request):
        raise NotImplementedError

    def get_limit(self, rule_type):
        if rule_type in self.settings.BRUTEFORCE_LIMITS:
            return self.settings.BRUTEFORCE_LIMITS[rule_type]
        return self.settings.BRUTEFORCE_LIMITS['default']

    def incr(self):
        if not self.key:
            return
        if self.connection.exists(self.key):
            self.connection.incr(self.key, 1)
        else:
            self.connection.set(self.key, 1)
            self.connection.expire(self.key, self.settings.TIMELIMIT * 60)

    def get_attempts(self):
        if not self.key:
            return 0
        data = self.connection.get(self.key)
        if not data:
            return 0
        return int(data)

    def log(self):
        # TODO: add logging
        pass

    def get_error(self):
        key = 'BRUTEFORCE_ERROR_{}'.format(self.name)
        return getattr(self.settings, key, self.settings.BRUTEFORCE_ERROR)

    def check(self):
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

    def get_value(self, request):
        if not request:
            return
        if not getattr(request, 'user'):
            return
        if not getattr(request, 'user'):
            return
        if not request.user.is_authenticated():
            return
        return request.user.pk


class IPChecker(BaseChecker):
    name = 'ip'

    def get_value(self, request):
        if not request:
            return
        return request.META['REMOTE_ADDR']


class CSRFChecker(BaseChecker):
    name = 'csrf'

    def get_value(self, request):
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
