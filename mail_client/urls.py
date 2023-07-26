from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .views import connexion, synchronization

urlpatterns = [
    path('auth-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('auth-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth-token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth-token/reject/', TokenBlacklistView.as_view(), name='token_reject'),
    path('connexions/', connexion.ListConnexionView.as_view(), name='list_connexion'),
    path('create-connexion/', connexion.CreateConnexionView.as_view(), name='create_connexion'),
    path('update-password/', connexion.UpdatePasswordView.as_view(), name='update_password'),
    path('update-connexion/', connexion.UpdateConnexionView.as_view(), name='update_connexion'),
    path('delete-connexion/', connexion.DeleteConnexionView.as_view(), name='delete_connexion'),
    path('test-synchronization/', synchronization.SynchronizeMailView.as_view(), name="test_sync")
]