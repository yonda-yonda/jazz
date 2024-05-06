from django.contrib import admin
from django.urls import include, path
# from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/v1/', include('v1.urls')),
]
