
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.models.order import Order
from product.models.category import Category
from product.models.product import Product
from django.contrib.auth import get_user_model


User = get_user_model()


class OrderViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="karol",
            password="123456",
        )

        self.product = Product.objects.create(
            title="Notebook",
            description="Notebook para estudos",
            price=3500,
            active=True,
        )

        self.order = Order.objects.create(user=self.user)
        self.order.product.add(self.product)

        self.client.force_authenticate(user=self.user)

    def test_list_orders(self):
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["total"], 3500)

    def test_orders_pagination(self):
        for _ in range(10):
            order = Order.objects.create(user=self.user)
            order.product.add(self.product)

        list_url = reverse("order-list")
        first_page = self.client.get(list_url)

        self.assertEqual(first_page.status_code, status.HTTP_200_OK)
        self.assertEqual(first_page.data["count"], 11)
        self.assertEqual(len(first_page.data["results"]), 10)
        self.assertIsNotNone(first_page.data["next"])

        second_page = self.client.get(list_url, {"page": 2})

        self.assertEqual(second_page.status_code, status.HTTP_200_OK)
        self.assertEqual(len(second_page.data["results"]), 1)
        self.assertIsNone(second_page.data["next"])
        self.assertIsNotNone(second_page.data["previous"])
