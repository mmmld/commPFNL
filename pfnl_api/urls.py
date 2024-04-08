from django.urls import path
from .views import (
    MemberListApiView, MemberRetrieveApiView, MemberRetrieveProductsApiView, ProductRetrieveApiView
)

urlpatterns = [
    path('member', MemberListApiView.as_view()),
    path('member/<str:phone>/', MemberRetrieveApiView.as_view()),
    path('member/<str:phone>/products/', MemberRetrieveProductsApiView.as_view()),
    path('product/<int:prod_id>/', ProductRetrieveApiView.as_view())
]
