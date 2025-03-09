from django.urls import path, include
from .views import UserViewSet, RegisterViewSet
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('users', UserViewSet, basename='urls')
router.register('register', RegisterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
