from django.apps import AppConfig


class FridgeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fridge_app'

    def ready(self):
        import fridge_app.signals