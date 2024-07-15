from django.apps import AppConfig


class BaseAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_analyzer'
