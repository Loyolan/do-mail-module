from django.test import TestCase
from rest_framework.test import APIClient
from mail_client.models import Connexion
import json

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
        response = client.post('/api/mail_clients/create-connexion/', json.dumps(data), content_type='application/json')
        # Response code should be 201
        self.assertEqual(response.status_code, 201)

        # Verify connexion created
        connexion = Connexion.objects.get(mail_address='user@example.com')
        self.assertEqual(connexion.domaine, 'example.com')
        self.assertEqual(connexion.port, 587)

