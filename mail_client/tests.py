from rest_framework.test import APIClient, APITestCase
from mail_client.models import Connexion
import json
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

#======================= UNIT TEST =================================#
# Test for creating connexion
class CreateConnexionViewTestCase(APITestCase):
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

# Test for changing connexion
class UpdatePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('token_obtain_pair')
        self.update_password_url = reverse('update_password')

        # Create a new connexion
        self.connexion = Connexion.objects.create_user(mail_address='user_pass@example.com', password='testpassword', domaine="example.com", port=587)

        # Obtain access token
        refresh = RefreshToken.for_user(self.connexion)
        self.token = str(refresh.access_token)

        # Force authentication
        self.client.force_authenticate(user=self.connexion, token=self.token)

    def test_update_password(self):
        data = {'new_password': 'testpassword1'}
        response = self.client.put(self.update_password_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

# Test for updating connexion information
class UpdateConnexionViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('token_obtain_pair')
        self.update_connexion_url = reverse('update_connexion')

        # Create a new connexion
        self.connexion = Connexion.objects.create_user(mail_address='user_infos@example.com', password='testpassword', domaine="example.com", port=587)

        # Obtain access token
        refresh = RefreshToken.for_user(self.connexion)
        self.token = str(refresh.access_token)

        # Force authentication
        self.client.force_authenticate(user=self.connexion, token=self.token)

    def test_update_infos(self):
        data = {'mail_address': 'kiadloyolan123@yahoo.fr', 'domaine': 'smtp.yahoo.com', 'port': 122 }
        response = self.client.put(self.update_connexion_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mail_address'], data['mail_address'])
        self.assertEqual(response.data['domaine'], data['domaine'])
        self.assertEqual(response.data['port'], data['port'])



# ====================== INTEGRATIONS TEST =========================#
# Test for generating jwt auth
class AuthTokenTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
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