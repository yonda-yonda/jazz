from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('books', views.BookViewSet)
router.register('publishers', views.PublisherViewSet)
router.register('authors', views.AuthorViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
