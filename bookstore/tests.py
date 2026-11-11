
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()

class TokenAuthenticationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="karol",
            password="123456",
        )

        self.token_url = reverse("api-token-auth")

    def test_obtain_auth_token(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "karol",
                "password": "123456",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        token = Token.objects.get(user=self.user)

        self.assertEqual(response.data["token"], token.key)

    def test_obtain_token_with_invalid_credentials(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "karol",
                "password": "senha_incorreta",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertNotIn("token", response.data)
