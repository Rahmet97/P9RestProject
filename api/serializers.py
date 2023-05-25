from rest_framework.serializers import ModelSerializer, Serializer, EmailField

from api.models import Product, Category, ShoppingCard


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerForCreate(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerForCard(ModelSerializer):

    class Meta:
        model = Product
        fields = ('title', 'price', 'category')


class ShoppingCardSerializer(ModelSerializer):
    class Meta:
        model = ShoppingCard
        fields = ('product', 'quantity',  'user', 'date')


class ShoppingCardForDetailSerializer(ModelSerializer):
    product = ProductSerializerForCard()

    class Meta:
        model = ShoppingCard
        fields = ('product', 'quantity')


class EmailSerializer(Serializer):
    email = EmailField()
