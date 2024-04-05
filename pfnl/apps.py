from django.apps import AppConfig


class PfnlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pfnl'
    
    def ready(self):
        from .signals import create_products_for_member
        from django.db.models.signals import post_save 
        from .models import Member
        post_save.connect(create_products_for_member, sender=Member)

