from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Cooperative, Member, Product
from django.db.models import Q

@receiver(pre_save, sender=Member)
def reset_telegram_id_on_phone_change(sender, instance, **kwargs):
  """
  When member changes their phone number, telegram_id is reset to 0
  """
  if instance.id:
     old = Member.objects.get(id=instance.id)
     if instance.member_phone != old.member_phone:
        instance.telegram_id = 0


@receiver(post_save, sender=Member)
def create_products_for_member(sender, instance, created, **kwargs):
  """
  When a new member is created, products of the cooperative type are automatically created and linked
  """
  if created:
    # Access the cooperative object
    cooperative = instance.coop
    # Create Product objects based on cooperative fields
    Product.objects.create(member=instance, prod_type=cooperative.offered_product_1)
    Product.objects.create(member=instance, prod_type=cooperative.offered_product_2)
    Product.objects.create(member=instance, prod_type=cooperative.offered_product_3)


@receiver(post_save, sender=Cooperative)
def update_products_on_cooperative_save(sender, instance, created, **kwargs):
  """
  If the product types of one cooperative changes, they are updated for all its members
  """
  if not created:  # Only handle updates, not creation
    # Get all members associated with this cooperative
    members = Member.objects.filter(coop=instance)
    product_types = [instance.offered_product_1, instance.offered_product_2, instance.offered_product_3]
    
    for member in members:
        product_types_of_member = set(member.product_set.values_list("prod_type", flat=True))
        products_to_remove = member.product_set.filter(~Q(prod_type__in=product_types))
        product_types_to_add = (set(product_types).union(product_types_of_member)).difference(product_types_of_member)

        for product in products_to_remove:
            product.delete()
        
        for product_type in product_types_to_add:
            Product.objects.create(member=member, prod_type=product_type)
    