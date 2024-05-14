from django.db import models
from .choices import PRODUCT_TYPES, ARTEMISIA_PRODUCTS
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Cooperative(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    coop_name = models.CharField("Nom de la coopérative", max_length=50)
    # coop_phone = models.CharField("Numéro de téléphone", max_length=14, unique=True)
    coop_phone = PhoneNumberField("Numéro de téléphone", blank=True, unique=True)
    offered_product_1 = models.CharField("Produit offert 1", max_length=10, choices=PRODUCT_TYPES, default="None")
    offered_product_2 = models.CharField("Produit offert 2", max_length=10, choices=PRODUCT_TYPES, default="None")
    offered_product_3 = models.CharField("Produit offert 3", max_length=10, choices=PRODUCT_TYPES, default="None")
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
    member_phone = PhoneNumberField("Numéro de téléphone", blank=True, unique=True)
    telegram_id = models.IntegerField("ID telegram", default=0)
    def __str__(self):
        return f'{self.member_name}'
    
    def get_coop_name(self):
         return self.coop.coop_name



class Product(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    prod_type = models.CharField("Type de produit", max_length=10)
    quantity = models.IntegerField("Quantité", default=0)
    last_modified = models.DateField("Dernière modification", auto_now_add=True)
    def __str__(self):
        return PRODUCT_TYPES[self.prod_type]


class ArtemisiaSeller(models.Model):
    name = models.CharField(max_length=200)
    phone = PhoneNumberField("Numéro de téléphone", blank=True, unique=True)
    telegram_id = models.IntegerField("ID telegram", default=0)

class ArtemisiaProduct(models.Model):
    seller = models.ForeignKey(ArtemisiaSeller, on_delete=models.CASCADE)
    prod_type = models.CharField("Type de produit", max_length=10, choices=ARTEMISIA_PRODUCTS, default="None")
    quantity = models.IntegerField("Quantité", default=0)
    price = models.IntegerField("Prix", default=0)
    last_modified = models.DateField("Dernière modification", auto_now_add=True)
    def __str__(self):
        return ARTEMISIA_PRODUCTS[self.prod_type]


