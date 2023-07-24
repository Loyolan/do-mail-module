from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Connexion
from .serializers import ConnexionSerializer, PasswordUpdateSerializer

from .permissions import IsAdminUser
from rest_framework.permissions import AllowAny

from django.contrib.auth.hashers import make_password

# LIST CONNEXIONS
class ListConnexionView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Connexion.objects.all()
    serializer_class = ConnexionSerializer

# CREATE NEW CONNEXION
class CreateConnexionView(generics.CreateAPIView):
    serializer_class = ConnexionSerializer
    queryset = Connexion.objects.all()
    serializer_class = ConnexionSerializer

    def create(self, request, *args, **kwargs):
        # Hash the password before saving it to the database
        password = request.data.get('password', None)
        if password:
            hashed_password = make_password(password)
            request.data['password'] = hashed_password

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# UPDATE USER PASSWORD
class UpdatePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"message": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)