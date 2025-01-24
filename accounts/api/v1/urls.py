from django.urls import path
from . import views


urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # change password
    # reset password
    # login token
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    
    # logout token
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    
    # login jwt
]

