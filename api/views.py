from django.db.models import Q, Sum
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Product, ShoppingCard
from api.permissions import IsAuthenticatedOrReadOnly2
from api.serializers import ProductSerializer, ProductSerializerForCreate, ShoppingCardSerializer, \
    ShoppingCardForDetailSerializer


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
    queryset = Product.objects.all()[:9]
    serializer_class = ProductSerializer
    permission_classes = ()


class AddToShoppingCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = ShoppingCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201)


class UserShoppingCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_products = ShoppingCard.objects.filter(user=request.user)
        serializer = ShoppingCardForDetailSerializer(user_products, many=True)
        summ = 0
        for element in serializer.data:
            summ += element['product']['price'] * element['quantity']
        data = {
            'data': serializer.data,
            'summ': summ
        }
        return Response(data)


class DeleteFromCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            ShoppingCard.objects.get(Q(pk=pk), Q(user=request.user)).delete()
        except ShoppingCard.DoesNotExist:
            return Response({'message': 'Bunday mahsulot mavjud emas'})
        return Response(status=204)