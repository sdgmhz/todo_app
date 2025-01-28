from django.urls import path, include
from . import views



urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('', include('django.contrib.auth.urls')),
    path('api/v1/', include('accounts.api.v1.urls')),

]