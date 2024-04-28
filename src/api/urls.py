from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('books', views.BookViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
