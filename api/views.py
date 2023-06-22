from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Q, Sum
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Product, ShoppingCard, UserData
from api.permissions import IsAuthenticatedOrReadOnly2
from api.serializers import ProductSerializer, ProductSerializerForCreate, ShoppingCardSerializer, \
    ShoppingCardForDetailSerializer, EmailSerializer, PhoneSerializer
from .tasks import send_email, send_sms

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = ()

    def get_queryset(self):
        if 'products' in cache:
            pass
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            cache.set('products', serializer.data, timeout=CACHE_TTL)
            return 

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST' or \
                self.request.method == 'PUT' or \
                self.request.method == 'PATCH':
            return ProductSerializerForCreate


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


class SendMail(APIView):
    permission_classes = ()

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            message = 'Test message'
            q = send_email.delay(email, message)
        except Exception as e:
            return Response({'success': False, 'message': f'{e}'})
        return Response({'success': True, 'message': 'Yuborildi'})


class SendVerificationCode(APIView):
    permission_classes = ()

    def post(self, request):
        phone = request.data['phone']
        user = UserData.objects.filter(phone=phone)
        if user:
            send_sms.delay(phone)
        else:
            return Response({'success': False, 'message': 'Bunday foydalanuvchi mavjud emas!'})
        return Response({'success': True, 'message': 'Yuborildi'})


class TestAPIView(APIView):
    permission_classes = ()

    def get(self, request):
        print(request.META.get('REMOTE_ADDR'))
        return Response({'remote_addr': request.META.get('REMOTE_ADDR')})