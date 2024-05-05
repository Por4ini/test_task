from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase



class AccountCreationTests(APITestCase):
    def test_create_account_success(self):
        url = reverse('user-list')
        data = {'email': 'testuser@mail.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_invalid_data(self):
        url = reverse('user-list')
        invalid_data = {'email': 'invalid_email', 'password': 'testpassword'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_duplicate_email(self):
        url = reverse('user-list')
        data = {'email': 'testuser@mail.com', 'password': 'testpassword'}
        self.client.post(url, data, format='json')  # Create the user first
        response = self.client.post(url, data, format='json')  # Try to create user with same email again
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_missing_data(self):
        url = reverse('user-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-list')
        self.jwt_create_url = reverse('jwt-create')
        self.valid_data = {'email': 'testuser@mail.com', 'password': 'testpassword'}
        self.invalid_data = {'email': 'testuser@mail.com', 'password': 'invalidpassword'}
        # Create a user with valid credentials
        self.client.post(self.register_url, self.valid_data, format='json')

    def test_jwt_token_creation(self):
        response = self.client.post(self.jwt_create_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_token_creation_invalid_credentials(self):
        response = self.client.post(self.jwt_create_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
