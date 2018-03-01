# django
from django.conf import LazySettings

from . import default_settings


class Settings(LazySettings):
    def __getattr__(self, name):
        return getattr(default_settings, name)


settings = Settings()
