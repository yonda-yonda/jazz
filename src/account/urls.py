from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register("auth", views.AuthViewSet, basename="auth")
router.register("token", views.TokenViewSet, basename="token")

urlpatterns = [
    path("", include(router.urls)),
]
