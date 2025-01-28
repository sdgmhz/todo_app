from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.DutyListView.as_view(), name="duty_list"),
    path("<int:pk>/", views.DutyDetailView.as_view(), name="duty_detail"),
    path("create/", views.DutyCreateView.as_view(), name="duty_create"),
    path("<int:pk>/update/", views.DutyUpdateView.as_view(), name="duty_update"),
    path("<int:pk>/delete/", views.DutyDeleteView.as_view(), name="duty_delete"),
    path(
        "<int:pk>/change_status/",
        views.ChangeStatusView.as_view(),
        name="change_status",
    ),
    path("api/v1/", include("duties.api.v1.urls")),
]
