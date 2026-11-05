from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from order.views import OrderViewSet
from product.views import CategoryViewSet, ProductViewSet

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]