from django.apps import AppConfig


class VigilanceappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'VigilanceAPP'

    def ready(self):
        import VigilanceAPP.signals
