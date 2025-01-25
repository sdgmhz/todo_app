from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # change password
    # reset password
    # login token
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    
    # logout token
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    
    # create jwt
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name="jwt-create"),

    # refresh jwt
    path('jwt/refresh/', TokenRefreshView.as_view(), name="jwt-refresh"),

    # verify jwt
    path('jwt/verify/', TokenVerifyView.as_view(), name="jwt-verify"),

]

