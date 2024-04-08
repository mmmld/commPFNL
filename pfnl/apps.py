from django.apps import AppConfig


class PfnlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pfnl'
    
    def ready(self):
        from .signals import create_products_for_member, update_products_on_cooperative_save
        from django.db.models.signals import post_save 
        from .models import Member, Cooperative
        post_save.connect(create_products_for_member, sender=Member)
        post_save.connect(update_products_on_cooperative_save, sender=Cooperative)

