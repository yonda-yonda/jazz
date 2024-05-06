from django.urls import path

from . import views 

urlpatterns = [
    path('services/', views.ServiceView.as_view({
    'get': 'list'
    })),
    path('services/<service_id>/', views.ServiceView.as_view({
    'get': 'retrieve'
    })),
    path('organizations/', views.OrganizationsRetriveView.as_view()),
    path('organizations/<organization_id>/', views.OrganizationRetriveView.as_view()),
    path('organizations/<organization_id>/members/', views.OrganizationMembersRetriveView.as_view()),
    path('organizations/<organization_id>/members/<user_id>/', views.OrganizationMemberRetriveView.as_view()),
]
