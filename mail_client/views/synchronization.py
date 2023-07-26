import smtplib
import email
import imaplib
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, validate_email
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from mail_client.models import Connexion
from mail_client.serializers import ConnexionSerializer

class SynchronizeMailView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConnexionSerializer

    def create(self, request, *args, **kwargs):
        mail_password = request.data.get('mail_password')

        # Get the currently authenticated user
        user = request.user

        # Validate the email address format
        try:
            validate_email(user.mail_address)
        except ValidationError:
            return Response({"error": "Invalid email address format."}, status=status.HTTP_400_BAD_REQUEST)

        imap = imaplib.IMAP4_SSL(user.domaine)
        imap.login(user.mail_address, mail_password)
        data = imap.select(mailbox='INBOX', readonly=False)
        print(data)
        # Return a success response
        return Response({"message": "Mail synchronization successful."}, status=status.HTTP_200_OK)
