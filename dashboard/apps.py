import warnings

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        # Remove warnings of the bunq sdk module
        warnings.filterwarnings(action='ignore', module='bunq')
