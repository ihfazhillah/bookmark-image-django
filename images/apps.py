from django.apps import AppConfig

class ImageConfig(AppConfig):
    name = 'images'
    verbose_name = 'Image Bookmarks'

    def ready(self):
        import images.signals
