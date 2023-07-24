from django.test import TestCase, Client
from rest_framework.test import APIClient
from mail_client.models import Connexion
import json
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

# Test for creating connexion
class CreateConnexionViewTestCase(TestCase):
    def test_create_connexion(self):
        # Create Client DRF
        client = APIClient()

        # Data for creating Connexion
        data = {
            'mail_address': 'user@example.com',
            'domaine': 'example.com',
            'port': 587,
            'password': 'password'
        }

        # Launch test
        url = reverse('create_connexion')
        response = client.post(url, json.dumps(data), content_type='application/json')
        # Response code should be 201
        self.assertEqual(response.status_code, 201)

        # Verify connexion created
        connexion = Connexion.objects.get(mail_address='user@example.com')
        self.assertEqual(connexion.domaine, 'example.com')
        self.assertEqual(connexion.port, 587)

# Test for generating jwt auth
class AuthTokenTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.connexion = Connexion.objects.create_user(mail_address='user_token@example.com', password='testpassword', domaine="example.com", port=587)
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

    def test_obtain_token(self):
        # Send POST method to url auth-token for getting token
        data = {'mail_address':'user_token@example.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        # Get token firts
        data = {'mail_address':'user_token@example.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        # Send POST method to url refresh-token
        token = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, json.dumps(token), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

        # Verify if new token is diffrent of refresh token
        new_access_token = response.data['access']
        self.assertNotEqual(refresh_token, new_access_token)