from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts.views.auth import UserAuthViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'accounts/auth', UserAuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
