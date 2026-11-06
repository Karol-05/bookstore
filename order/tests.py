from django.test import TestCase
from django.contrib.auth.models import User

from product.models.product import Product
from product.models.category import Category
from order.models.order import Order
from order.serializers.order_serializers import OrderSerializer


class OrderSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="karol",
            password="123456"
        )

        self.category = Category.objects.create(
            title="Eletrônicos",
            slug="eletronicos",
            description="Produtos eletrônicos",
            active=True
        )

        self.product1 = Product.objects.create(
            title="Notebook",
            description="Notebook para estudos",
            price=3500,
            active=True
        )

        self.product2 = Product.objects.create(
            title="Mouse",
            description="Mouse sem fio",
            price=150,
            active=True
        )

        self.product1.category.add(self.category)
        self.product2.category.add(self.category)

        self.order = Order.objects.create(
            user=self.user
        )

        self.order.product.add(
            self.product1,
            self.product2
        )

    def test_order_serializer_valid_data(self):
        data = {
            "product": [
                {
                    "title": "Teclado",
                    "description": "Teclado mecânico",
                    "price": 250,
                    "active": True,
                    "category": [
                        {
                            "title": "Eletrônicos",
                            "slug": "teclados",
                            "description": "Produtos eletrônicos",
                            "active": True
                        }
                    ]
                }
            ]
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_order_serializer_product_required(self):
        data = {}

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("product", serializer.errors)

    def test_order_serializer_invalid_product(self):
        data = {
            "product": [
                {
                    "description": "Produto sem título",
                    "price": 100,
                    "active": True,
                    "category": []
                }
            ]
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("product", serializer.errors)

    def test_order_serializer_expected_fields(self):
        serializer = OrderSerializer(instance=self.order)

        expected_fields = [
            "product",
            "total"
        ]

        self.assertEqual(
            list(serializer.data.keys()),
            expected_fields
        )

    def test_order_serializer_product_relationship(self):
        serializer = OrderSerializer(instance=self.order)

        self.assertEqual(
            len(serializer.data["product"]),
            2
        )

    def test_order_serializer_total(self):
        serializer = OrderSerializer(instance=self.order)

        self.assertEqual(
            serializer.data["total"],
            3650
        )