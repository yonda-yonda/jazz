from rest_framework import generics, permissions, viewsets

from account.models import Service, Organization, User
from .serializer import ServiceSerializer, OrganizationSerializer, OrganizationMemberSerializer
from .permissions import IsOrganizationMember, IsOrganizationAdmin, IsUserSelf


class ServiceView(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_url_kwarg = 'service_id'

class OrganizationsRetriveView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationRetriveView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser | IsOrganizationMember,)
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_url_kwarg = 'organization_id'

class OrganizationMembersRetriveView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser | IsOrganizationAdmin,)
    serializer_class = OrganizationMemberSerializer

    def get_queryset(self):
        organization_id = self.request.parser_context['kwargs']['organization_id']
        queryset = User.objects.prefetch_related("membership").filter(membership__organization=organization_id)
        return queryset

class OrganizationMemberRetriveView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser | IsOrganizationAdmin | IsUserSelf,)
    serializer_class = OrganizationMemberSerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        organization_id = self.request.parser_context['kwargs']['organization_id']
        queryset = User.objects.prefetch_related("membership").filter(membership__organization=organization_id)
        return queryset