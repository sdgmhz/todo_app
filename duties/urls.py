from django.urls import path
from . import views

urlpatterns = [
    path('', views.DutyListView.as_view(), name='duty_list'),
    path('<int:pk>/', views.DutyDetailView.as_view(), name='duty_detail'),
    path('create/', views.DutyCreateView.as_view(), name="duty_create"),
    path('<int:pk>/update/', views.DutyUpdateView.as_view(), name="duty_update"),
    path('<int:pk>/delete/', views.DutyDeleteView.as_view(), name="duty_delete"),
    
]