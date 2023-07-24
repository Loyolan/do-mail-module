
from rest_framework import serializers
from .models import Connexion

class ConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connexion
        fields = ['id', 'mail_address', 'domaine', 'port', 'password', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}