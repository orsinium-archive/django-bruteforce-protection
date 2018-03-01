# django
from django.conf import settings as _settings

from . import default_settings


class Settings(object):
    def __getattr__(self, name):
        try:
            return getattr(_settings, name)
        except AttributeError:
            pass
        return getattr(default_settings, name)


settings = Settings()
