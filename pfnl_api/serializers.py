from rest_framework import serializers

from pfnl.models import Cooperative, Member, Product, ArtemisiaSeller, ArtemisiaProduct

class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = ["coop_name", "coop_phone", "offered_product_1", "offered_product_2", "offered_product_3"]

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "member_name", "member_phone", "coop", "telegram_id"]
        depth = 1

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "member", "prod_type", "quantity", "last_modified"]

class ArtemisiaSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtemisiaSeller
        fields = ["id", "name", "phone", "telegram_id"]

class ArtemisiaProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtemisiaProduct
        fields = ["id", "seller", "prod_type", "quantity", "price", "last_modified"]