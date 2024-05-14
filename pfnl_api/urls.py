from django.urls import path
from .views import *

urlpatterns = [
    # ---------- NTFP ---------------------
    path('member', MemberListApiView.as_view()),
    path('member/look_for/', MemberSearchApiView.as_view()),
    path('member/<int:member_id>/', MemberEditApiView.as_view()),
    path('member/<int:telegram_id>/products/', MemberRetrieveProductsApiView.as_view()),
    path('product/<int:prod_id>/', ProductRetrieveApiView.as_view()),

    # ---------- ARTEMISIA -------------

    path('seller/look_for/', ArtemisiaSellerSearchApiView.as_view()),
    path('seller/<int:seller_id>/', ArtemisiaSellerEditApiView.as_view()),
    path('seller/<int:telegram_id>/products/', ArtemisiaSellerRetrieveProductsApiView.as_view()),
    path('artemisia_product/<int:prod_id>/', ArtemisiaProductRetrieveApiView.as_view())
]
