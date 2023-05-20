from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Product
from api.permissions import IsAuthenticatedOrReadOnly2
from api.serializers import ProductSerializer, ProductSerializerForCreate


class ProductAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly2,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST':
            return ProductSerializerForCreate

    def get_permission_classes(self):
        if self.request.method == 'GET':
            return tuple()
        else:
            return (IsAuthenticated,)

class ProductUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = ()
