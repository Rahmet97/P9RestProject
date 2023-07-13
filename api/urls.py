from django.urls import path, include

from api.views import ProductViewSet, AddToShoppingCardAPIView, UserShoppingCardAPIView, \
    DeleteFromCardAPIView, SendMail, SendVerificationCode, TestAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    # path('products', ProductAPIView.as_view(), name='products'),
    path('add-to-card', AddToShoppingCardAPIView.as_view(), name='shopping_card'),
    path('user-card', UserShoppingCardAPIView.as_view(), name='user_card'),
    path('user-card-delete/<int:pk>', DeleteFromCardAPIView.as_view(), name='user_card_delete'),
    path('send-email', SendMail.as_view(), name='send_email'),
    path('verification', SendVerificationCode.as_view(), name='verification'),
    path('testing', TestAPIView.as_view(), name='test'),
    # path('product-update-delete/<int:pk>', ProductUpdateDeleteAPIView.as_view(), name='products_update_delete'),
    path('', include(router.urls))
]
