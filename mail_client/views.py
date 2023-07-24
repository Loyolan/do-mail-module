from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class SecretDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        secret_data = "This is some secret data!"
        return Response({"data": secret_data})