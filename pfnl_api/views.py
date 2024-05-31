from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import permissions
from pfnl.models import Cooperative, Member, Product, ArtemisiaSeller, ArtemisiaProduct
from .serializers import CooperativeSerializer, MemberSerializer, ProductSerializer, ArtemisiaProductSerializer, ArtemisiaSellerSerializer

from django.db.models import Q

from django.utils import timezone

class MemberListApiView(APIView):
    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MemberSearchApiView(APIView):
    def get(self, request, *args, **kwargs):
            try:
                phone = request.data.get('phone')
                # member = Member.objects.get(member_phone=phone)
                member = Member.objects.filter(Q(member_phone__icontains=phone)).first()
                if member == None:
                     return Response(
                        {"res": "Member with this phone number does not exist."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                serializer = MemberSerializer(member)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Member.DoesNotExist:
                 return Response(
                    {"res": "Member with this phone number does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )


class MemberEditApiView(APIView):
    def get(self, request, member_id, *args, **kwargs):
        try:
            member = Member.objects.get(telegram_id=member_id)
            serializer = MemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response(
                                {"res": "Member with this ID does not exist."},
                                status=status.HTTP_400_BAD_REQUEST
                            )

    def put(self, request, member_id, *args, **kwargs):
        try:
            member = Member.objects.get(id=member_id)
            data = {
                     'telegram_id': request.data.get('telegram_id'),
                }
            serializer = MemberSerializer(instance = member, data=data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Member.DoesNotExist:
            return Response(
                                {"res": "Member with this ID does not exist."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
    
    

class MemberRetrieveProductsApiView(APIView):
    def get(self, request, telegram_id, *args, **kwargs):
        member = Member.objects.get(telegram_id=telegram_id)
        if member == None:
                return Response(
                {"res": "Member with this phone number does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = member.product_set.all()
                
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

            
class ProductRetrieveApiView(APIView):

     def get(self, request, prod_id, *args, **kwargs):
            try:
                product = Product.objects.get(id=prod_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Product.DoesNotExist:
                return Response(
                                    {"res": "Product with this ID does not exist."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )

     def put(self, request, prod_id, *args, **kwargs):
            try:
                product = Product.objects.get(id=prod_id)
                data = {
                     'quantity': request.data.get('quantity'),
                     'last_modified': timezone.now()
                }
                serializer = ProductSerializer(instance = product, data=data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Product.DoesNotExist:
                return Response(
                                    {"res": "Product with this ID does not exist."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )

class CooperativeRetrieveApiView(APIView):
     def get(self, request, coop_id, *args, **kwargs):
            try:
                coop = Cooperative.objects.get(id=coop_id)
                serializer = CooperativeSerializer(coop)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Cooperative.DoesNotExist:
                return Response(
                                    {"res": "Cooperative with this ID does not exist."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )


# ----------------------- ARTEMISIA --------------------------------------

class ArtemisiaSellerSearchApiView(APIView):
    def get(self, request, *args, **kwargs):
            try:
                phone = request.data.get('phone')
                seller = ArtemisiaSeller.objects.filter(Q(phone__icontains=phone)).first()
                if seller == None:
                     return Response(
                        {"res": "Seller with this phone number does not exist."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                serializer = ArtemisiaSellerSerializer(seller)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ArtemisiaSeller.DoesNotExist:
                 return Response(
                    {"res": "Seller with this phone number does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            

class ArtemisiaSellerEditApiView(APIView):
    def get(self, request, seller_id, *args, **kwargs):
        try:
            seller = ArtemisiaSeller.objects.get(telegram_id=seller_id)
            serializer = ArtemisiaSellerSerializer(seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArtemisiaSeller.DoesNotExist:
            return Response(
                                {"res": "Seller with this ID does not exist."},
                                status=status.HTTP_400_BAD_REQUEST
                            )

    def put(self, request, seller_id, *args, **kwargs):
        try:
            seller = ArtemisiaSeller.objects.get(id=seller_id)
            data = {
                     'telegram_id': request.data.get('telegram_id'),
                }
            serializer = ArtemisiaSellerSerializer(instance = seller, data=data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ArtemisiaSeller.DoesNotExist:
            return Response(
                                {"res": "Seller with this ID does not exist."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
        
class ArtemisiaSellerRetrieveProductsApiView(APIView):
    def get(self, request, telegram_id, *args, **kwargs):
        seller = ArtemisiaSeller.objects.get(telegram_id=telegram_id)
        if seller == None:
                return Response(
                {"res": "Seller with this phone number does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = seller.artemisiaproduct_set.all()
                
        serializer = ArtemisiaProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ArtemisiaProductRetrieveApiView(APIView):

     def get(self, request, prod_id, *args, **kwargs):
            try:
                product = ArtemisiaProduct.objects.get(id=prod_id)
                serializer = ArtemisiaProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except ArtemisiaProduct.DoesNotExist:
                return Response(
                                    {"res": "Product with this ID does not exist."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )

     def put(self, request, prod_id, *args, **kwargs):
            try:
                product = ArtemisiaProduct.objects.get(id=prod_id)
                data = {
                     'quantity': request.data.get('quantity'),
                     'price': request.data.get('price'),
                     'last_modified': timezone.now()
                }
                serializer = ArtemisiaProductSerializer(instance = product, data=data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except ArtemisiaProduct.DoesNotExist:
                return Response(
                                    {"res": "Product with this ID does not exist."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
