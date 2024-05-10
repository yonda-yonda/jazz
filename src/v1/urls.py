from django.urls import path, include
from rest_framework_nested import routers

from . import views 

router = routers.SimpleRouter()
router.register("services", views.ServiceViewSet)
router.register("organizations", views.OrganizationRetrieveView)

organization_router = routers.NestedSimpleRouter(router, "organizations",
    lookup="organization")
organization_router.register("members", views.OrganizationMemberViewSet, 
    basename="organization-member")

organization_router.register(
    "services", views.OrganizationServiceViewSet, basename="organization-service"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(organization_router.urls)),
]
