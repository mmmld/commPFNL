from django.db import models
from .choices import PRODUCT_TYPES
from django.contrib.auth.models import User

# TODO: add validator for the phone field/make sure it is the correct type

class Cooperative(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    coop_name = models.CharField("Nom de la coopérative", max_length=50)
    coop_phone = models.CharField("Numéro de téléphone", max_length=14, unique=True)
    offered_product_1 = models.CharField("Produit offert 1", max_length=10, choices=PRODUCT_TYPES, default="None")
    offered_product_2 = models.CharField("Produit offert 2", max_length=10, choices=PRODUCT_TYPES, default="None")
    offered_product_3 = models.CharField("Produit offert 1", max_length=10, choices=PRODUCT_TYPES, default="None")
    def __str__(self):
        return self.coop_name
    
    def get_total_quantity_first_product(self):
            all_quantities = Product.objects.filter(member__coop=self).filter(prod_type=self.offered_product_1).values_list("quantity", flat=True)
            return sum(all_quantities)
    
    def get_total_quantity_second_product(self):
            all_quantities = Product.objects.filter(member__coop=self).filter(prod_type=self.offered_product_2).values_list("quantity", flat=True)
            return sum(all_quantities)
    
    def get_total_quantity_third_product(self):
            all_quantities = Product.objects.filter(member__coop=self).filter(prod_type=self.offered_product_3).values_list("quantity", flat=True)
            return sum(all_quantities)


class Member(models.Model):
    coop = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    member_name = models.CharField("Nom du membre", max_length=50)
    member_phone = models.CharField("Numéro de téléphone", max_length=14, unique=True)
    def __str__(self):
        return f'{self.member_name}'
    
    def get_coop_name(self):
         return self.coop.coop_name




class Product(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    prod_type = models.CharField("Type de produit", max_length=10, editable=False)
    quantity = models.IntegerField("Quantité", default=0)
    last_modified = models.DateField("Dernière modification", auto_now_add=True)
    def __str__(self):
        return PRODUCT_TYPES[self.prod_type]


