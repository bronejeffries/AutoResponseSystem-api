from django.apps import AppConfig


class ModeratorConfig(AppConfig):
    name = 'moderator'

    def ready(self):
        from . import signals
