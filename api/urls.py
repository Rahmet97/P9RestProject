from django.urls import path

from api.views import ProductAPIView, ProductUpdateDeleteAPIView

urlpatterns = [
    path('products', ProductAPIView.as_view(), name='products'),
    path('product-update-delete/<int:pk>', ProductUpdateDeleteAPIView.as_view(), name='products_update_delete'),
]