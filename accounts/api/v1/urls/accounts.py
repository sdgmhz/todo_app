from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)



urlpatterns = [

    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # change password
    path('change-password/', views.ChangePasswordApiView.as_view(), name="change-password"),

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

    # activation
    path('activation/confirm/<str:token>/', views.ActivationApiView.as_view(), name='activation'),

    # activation resend
    path('activation/resend/', views.ActivationResendApiView.as_view(), name='activation-resend'),

    # password reset request
    path('password/reset/',views.PasswordResetApiView.as_view(), name='password-reset'),

    # password reset confirm
    path('password/reset/confirm/<str:token>/', views.PasswordResetConfirmApiView.as_view(), name="password-reset-confirm"),

    
]

