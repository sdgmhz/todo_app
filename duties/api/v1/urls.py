from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

app_name = 'api-v1'

""" create a router for duty urls"""
router = DefaultRouter()
router.register('duty', views.DutyModelViewSet, basename='duty')
urlpatterns = router.urls


