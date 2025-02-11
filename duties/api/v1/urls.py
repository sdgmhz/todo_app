from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

app_name = "api-v1"

""" create a router for duty urls"""
router = DefaultRouter()
router.register("duty", views.DutyModelViewSet, basename="duty")
urlpatterns = router.urls

urlpatterns += [
    path('weather/', views.WeatherCacheApiView.as_view(), name='weather'),
]
