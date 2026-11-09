from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.models.order import Order
from product.models.category import Category
from product.models.product import Product

class OrderViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="karol",
            password="test-password",
        )

        self.category = Category.objects.create(
            title="Eletrônicos",
            slug="eletronicos",
        )

        self.product = Product.objects.create(
            title="Notebook",
            description="Notebook para estudos",
            price=3500,
            active=True,
        )

        self.product.category.add(self.category)

        self.order = Order.objects.create(user=self.user)
        self.order.product.add(self.product)

        self.client.force_authenticate(user=self.user)

    def test_list_orders(self):
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["total"], 3500)

    def test_retrieve_order(self):
        response = self.client.get(
            reverse(
                "order-detail",
                kwargs={"pk": self.order.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 3500)
        self.assertEqual(
            response.data["product"][0]["title"],
            "Notebook",
        )

    def test_order_not_found(self):
        response = self.client.get(
            reverse(
                "order-detail",
                kwargs={"pk": 99999},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )