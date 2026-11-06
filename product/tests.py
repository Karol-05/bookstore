from django.test import TestCase

from product.models.product import Product
from product.models.category import Category
from product.serializers.product_serializers import ProductSerializer
from product.serializers.category_serializers import CategorySerializer


class CategorySerializerTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title="Eletrônicos",
            slug="eletronicos",
            description="Produtos eletrônicos",
            active=True
        )

    def test_category_serializer_valid_data(self):
        data = {
            "title": "Informática",
            "slug": "informatica",
            "description": "Produtos de informática",
            "active": True
        }

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_category_serializer_required_fields(self):
        data = {
            "description": "Categoria sem título"
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("slug", serializer.errors)

    def test_category_serializer_invalid_slug(self):
        data = {
            "title": "Categoria inválida",
            "slug": "categoria inválida!"
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)

    def test_category_serializer_expected_fields(self):
        serializer = CategorySerializer(instance=self.category)

        expected_fields = [
            "title",
            "slug",
            "description",
            "active"
        ]

        self.assertEqual(
            list(serializer.data.keys()),
            expected_fields
        )


class ProductSerializerTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title="Eletrônicos",
            slug="eletronicos",
            description="Produtos eletrônicos",
            active=True
        )

        self.product = Product.objects.create(
            title="Notebook",
            description="Notebook para estudos",
            price=3500,
            active=True
        )

        self.product.category.add(self.category)

    def test_product_serializer_valid_data(self):
        data = {
            "title": "Mouse",
            "description": "Mouse sem fio",
            "price": 150,
            "active": True,
            "category": [
                {
                    "title": "Acessórios",
                    "slug": "acessorios",
                    "description": "Acessórios de informática",
                    "active": True
                }
            ]
        }

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_product_serializer_required_title(self):
        data = {
            "description": "Produto sem título",
            "price": 100,
            "active": True,
            "category": []
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_product_serializer_invalid_category(self):
        data = {
            "title": "Teclado",
            "description": "Teclado mecânico",
            "price": 200,
            "active": True,
            "category": [
                {
                    "title": "Categoria sem slug",
                    "description": "Descrição",
                    "active": True
                }
            ]
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)

    def test_product_serializer_expected_fields(self):
        serializer = ProductSerializer(instance=self.product)

        expected_fields = [
            "title",
            "description",
            "price",
            "active",
            "category"
        ]

        self.assertEqual(
            list(serializer.data.keys()),
            expected_fields
        )

    def test_product_serializer_category_relationship(self):
        serializer = ProductSerializer(instance=self.product)

        self.assertEqual(
            len(serializer.data["category"]),
            1
        )

        self.assertEqual(
            serializer.data["category"][0]["title"],
            "Eletrônicos"
        )