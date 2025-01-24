from django.urls import path
from . import views

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),
    
    # change password
    # reset password
    # login token
    # login jwt
]

