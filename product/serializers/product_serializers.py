from rest_fremework import serializers
from product.models.product import Product
from product.serializers.category_serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'active',
            'category'
        ]