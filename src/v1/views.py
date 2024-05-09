from rest_framework import generics, permissions, viewsets, serializers, status
from rest_framework.response import Response

from account.models import Service, Organization, User, Membership
from .serializer import (
    ServiceSerializer,
    OrganizationSerializer, 
    OrganizationMemberSerializer, 
    OrganizationMemberCreateSerializer,
    OrganizationMemberUpdateSerializer,
    MembershipSerializer,
    EmptySerializer
)
from .permissions import IsOrganizationMember, IsOrganizationAdmin, IsUserSelf


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_url_kwarg = 'service_id'


class OrganizationRetrieveView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAdminUser | IsOrganizationMember,)
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_url_kwarg = "organization_id"

    def get_permissions(self):
        premissions = (permissions.IsAdminUser,)
        if self.action == "retrieve":
            premissions = (permissions.IsAdminUser | IsOrganizationAdmin,)
        return [permission() for permission in premissions]


class OrganizationMemberViewSet(viewsets.ModelViewSet):
    lookup_url_kwarg = 'user_id'

    def get_permissions(self):
        premissions = (permissions.IsAdminUser | IsOrganizationAdmin,)
        if self.action == 'retrieve':
            premissions = (permissions.IsAdminUser | IsOrganizationAdmin | IsUserSelf,)
        return [permission() for permission in premissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return OrganizationMemberCreateSerializer
        if self.action in ['update', 'partial_update']:
            return OrganizationMemberUpdateSerializer

        return OrganizationMemberSerializer    

    def get_queryset(self):
        organization_id = self.request.parser_context['kwargs']['organization_id']
        queryset = User.objects.prefetch_related('membership', 'membership__organization').filter(membership__organization=organization_id)
        return queryset

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        organization_id = self.request.parser_context['kwargs']['organization_id']
        user_id = input_serializer.data['id']
        role = input_serializer.data['role']
        try:
            user = User.objects.prefetch_related('membership').get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User dosen\'t exist.')

        try:
            if user.membership:
                return Response({'message':'User already has membership to any organization.'}, status=status.HTTP_409_CONFLICT)
        except Membership.DoesNotExist:
            serializer = MembershipSerializer(data={'role':role, 'organization': organization_id, 'user': user_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            data = {
                'id': user.id,
                'email': user.email,
                'role': role
            }
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        role = input_serializer.data['role']

        user = self.get_object()
        serializer = MembershipSerializer(instance=user.membership, data={'role':role}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'id': user.id,
            'email': user.email,
            'role': role
        }
        return Response(data)


class OrganizationServiceViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAdminUser | IsOrganizationMember,)
    queryset = Organization.objects.prefetch_related('services').all()
    serializer_class = EmptySerializer
    lookup_url_kwarg = 'organization_id'

    def create(self, request, *args, **kwargs):
        service_id = self.request.parser_context['kwargs']['service_id']
        filter_kwargs = {'id': service_id}
        service = generics.get_object_or_404(Service.objects.all(), **filter_kwargs)

        organization = self.get_object()
        services = organization.services.all()
        if services.filter(id=service_id).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        organization.services.add(service)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        service_id = self.request.parser_context['kwargs']['service_id']
        filter_kwargs = {'id': service_id}
        service = generics.get_object_or_404(Service.objects.all(), **filter_kwargs)

        organization = self.get_object()
        services = organization.services.all()
        if not services.filter(id=service_id).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        organization.services.remove(service)

        return Response(status=status.HTTP_204_NO_CONTENT)
