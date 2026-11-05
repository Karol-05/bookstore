from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from product.models.category import Category
from product.models.product import Product
from product.serializers.category_serializers import CategorySerializer
from product.serializers.product_serializers import ProductSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer

class ProductViewSet(ReadOnlyModelViewSet):
    queryset = (
        Product.objects.all()
        .prefetch_related("category")
        .order_by("id")
    )
    serializer_class = ProductSerializer