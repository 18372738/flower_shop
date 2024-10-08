from django.apps import AppConfig


class FlowerModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flower_models'

    def ready(self):
        import flower_models.signals
