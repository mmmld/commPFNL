from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import permissions
from pfnl.models import Member, Product
from .serializers import MemberSerializer, ProductSerializer

from django.utils import timezone

class MemberListApiView(APIView):

    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MemberRetrieveApiView(APIView):

    def get(self, request, phone, *args, **kwargs):
            try:
                member = Member.objects.get(member_phone=phone)                 
                serializer = MemberSerializer(member)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Member.DoesNotExist:
                 return Response(
                    {"res": "Member with this phone number does not exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
    

class MemberRetrieveProductsApiView(APIView):

    def get(self, request, phone, *args, **kwargs):
            member = Member.objects.filter(member_phone=phone).first()
            if member == None:
                 return Response(
                    {"res": "Member with this phone number does not exists"},
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
                                    {"res": "Product with this ID does not exists"},
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
                                    {"res": "Product with this ID does not exists"},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
