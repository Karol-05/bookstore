from rest_framework.viewsets import ReadOnlyModelViewSet

from order.models.order import Order
from order.serializers.order_serializers import OrderSerializer

class OrderViewSet(ReadOnlyModelViewSet):
    queryset = (
        Order.objects.all()
        .select_related("user")
        .prefetch_related("product__category")
        .order_by("id")
    )
    serializer_class = OrderSerializer