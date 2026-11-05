from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.models.category import Category
from product.models.product import Product

class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title="Eletrônicos",
            slug="eletronicos",
            description="Produtos eletrônicos",
            active=True,
        )

        self.list_url = reverse("category-list")
        self.detail_url = reverse(
            "category-detail",
            kwargs={"pk": self.category.pk},
        )

    def test_list_categories(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "eletronicos")

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Eletrônicos")

    def test_create_category(self):
        data = {
            "title": "Informática",
            "slug": "informatica",
            "description": "Acessórios de informática",
            "active": True,
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Category.objects.filter(slug="informatica").exists()
        )

    def test_update_category(self):
        response = self.client.patch(
            self.detail_url,
            {"title": "Eletrônicos e tecnologia"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.category.refresh_from_db()

        self.assertEqual(
            self.category.title,
            "Eletrônicos e tecnologia",
        )

    def test_delete_category(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Category.objects.filter(pk=self.category.pk).exists()
        )

class ProductViewSetTest(APITestCase):

    def setUp(self):
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

    def test_list_products(self):
        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Notebook")

    def test_retrieve_product_includes_categories(self):
        response = self.client.get(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["category"][0]["slug"],
            "eletronicos",
        )