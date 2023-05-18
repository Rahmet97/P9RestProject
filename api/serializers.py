from rest_framework.serializers import ModelSerializer

from api.models import Product


class ProductSerializer(ModelSerializer):

    # def create(self, validated_data):
    #     return Product.objects.create(**validated_data)

    class Meta:
        model = Product
        fields = '__all__'
