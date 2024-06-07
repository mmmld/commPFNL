from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

POSSIBLE_STATES = ["contact", "product_list", "product", "quantity", "price", "confirm", "generate_communique"]

class State(models.Model):
    telegram_id = models.IntegerField("ID telegram", default=0, unique=True)
    state = models.CharField("State", max_length=20, default="None")
    time_set = models.DateTimeField("Time set", auto_now=True)
    product = models.CharField("Product", max_length=50)
    quantity = models.IntegerField("Quantity", default=0)
    price = models.IntegerField("Price", default=0)