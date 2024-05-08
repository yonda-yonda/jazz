from django.urls import path

from . import views 

urlpatterns = [
    path('services/', views.ServiceViewSet.as_view({
        'get': 'list'
    })),
    path('services/<service_id>/', views.ServiceViewSet.as_view({
        'get': 'retrieve'
    })),
    path('organizations/', views.OrganizationsRetrieveView.as_view()),
    path('organizations/<organization_id>/', views.OrganizationRetrieveView.as_view()),
    path('organizations/<organization_id>/members/', views.OrganizationMemberViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('organizations/<organization_id>/members/<user_id>/', views.OrganizationMemberViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
]
