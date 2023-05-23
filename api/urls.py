from django.urls import path

from api.views import ProductAPIView, ProductUpdateDeleteAPIView, AddToShoppingCardAPIView, UserShoppingCardAPIView, \
    DeleteFromCardAPIView

urlpatterns = [
    path('products', ProductAPIView.as_view(), name='products'),
    path('add-to-card', AddToShoppingCardAPIView.as_view(), name='shopping_card'),
    path('user-card', UserShoppingCardAPIView.as_view(), name='user_card'),
    path('user-card-delete/<int:pk>', DeleteFromCardAPIView.as_view(), name='user_card_delete'),
    path('product-update-delete/<int:pk>', ProductUpdateDeleteAPIView.as_view(), name='products_update_delete'),
]