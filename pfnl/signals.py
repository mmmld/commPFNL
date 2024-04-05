from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cooperative, Member, Product
from django.db.models import Q

@receiver(post_save, sender=Member)
def create_products_for_member(sender, instance, created, **kwargs):
  if created:
    # Access the cooperative object
    cooperative = instance.coop
    # Create Product objects based on cooperative fields
    Product.objects.create(member=instance, prod_type=cooperative.offered_product_1)
    Product.objects.create(member=instance, prod_type=cooperative.offered_product_2)
    Product.objects.create(member=instance, prod_type=cooperative.offered_product_3)


@receiver(post_save, sender=Cooperative)
def update_products_on_cooperative_save(sender, instance, created, **kwargs):
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
    
    
