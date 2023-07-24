
from rest_framework import serializers
from .models import Connexion

class ConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connexion
        fields = ['id', 'mail_address', 'domaine', 'port', 'password', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}


class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance

class ConnexionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connexion
        fields = ['mail_address', 'domaine', 'port']