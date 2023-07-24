from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('auth-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('auth-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('connexions/', views.ListConnexionView.as_view(), name='list_connexion'),
    path('create_connexion/', views.CreateConnexionView.as_view(), name='create_connexion')
]