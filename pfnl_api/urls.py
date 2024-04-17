from django.urls import path
from .views import *

urlpatterns = [
    path('member', MemberListApiView.as_view()),
    path('member/look_for/', MemberSearchApiView.as_view()),
    path('member/<int:member_id>/', MemberEditApiView.as_view()),
    path('member/<int:telegram_id>/products/', MemberRetrieveProductsApiView.as_view()),
    path('product/<int:prod_id>/', ProductRetrieveApiView.as_view())
]
