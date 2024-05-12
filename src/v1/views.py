from rest_framework import (
    authentication,
    generics,
    permissions,
    viewsets,
    serializers,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from account.models import Service, Organization, User, Membership
from .serializer import (
    ServiceSerializer,
    OrganizationSerializer,
    OrganizationMemberSerializer,
    OrganizationMemberCreateSerializer,
    OrganizationMemberUpdateSerializer,
    MembershipSerializer,
)
from .permissions import getIsOrganizationMember, getIsOrganizationAdmin, getIsUserSelf

authentication_classes = (
    authentication.TokenAuthentication,
    authentication.SessionAuthentication,
)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = authentication_classes
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OrganizationRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = authentication_classes
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    organization_pk = "pk"

    def get_permissions(self):
        premissions = (permissions.IsAdminUser,)
        if self.action == "retrieve":
            premissions = (
                permissions.IsAdminUser | getIsOrganizationMember(self.organization_pk),
            )
        return [permission() for permission in premissions]


class OrganizationMemberViewSet(viewsets.ModelViewSet):
    authentication_classes = authentication_classes
    organization_pk = "organization_pk"
    user_pk = "pk"

    def get_permissions(self):
        premissions = (
            permissions.IsAdminUser | getIsOrganizationAdmin(self.organization_pk),
        )
        if self.action == "retrieve":
            premissions = (
                permissions.IsAdminUser
                | getIsOrganizationAdmin(self.organization_pk)
                | getIsUserSelf(self.user_pk),
            )
        return [permission() for permission in premissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "create":
            return OrganizationMemberCreateSerializer
        if self.action in ["update", "partial_update"]:
            return OrganizationMemberUpdateSerializer

        return OrganizationMemberSerializer

    def get_queryset(self):
        organization_id = self.request.parser_context["kwargs"][self.organization_pk]
        queryset = User.objects.prefetch_related(
            "membership", "membership__organization"
        ).filter(membership__organization=organization_id)
        return queryset

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        organization_id = self.request.parser_context["kwargs"][self.organization_pk]
        user_id = input_serializer.data["id"]
        role = input_serializer.data["role"]
        try:
            user = User.objects.prefetch_related("membership").get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User dosen't exist.")

        try:
            if user.membership:
                return Response(
                    {"message": "User already has membership to any organization."},
                    status=status.HTTP_409_CONFLICT,
                )
        except Membership.DoesNotExist:
            serializer = MembershipSerializer(
                data={"role": role, "organization": organization_id, "user": user_id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            data = {"id": user.id, "email": user.email, "role": role}
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        role = input_serializer.data["role"]

        user = self.get_object()
        serializer = MembershipSerializer(
            instance=user.membership, data={"role": role}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"id": user.id, "email": user.email, "role": role}
        return Response(data)


class OrganizationServiceViewSet(viewsets.ViewSet):
    authentication_classes = authentication_classes
    organization_pk = "organization_pk"
    service_pk = "pk"

    queryset = Service.objects.all()

    def get_permissions(self):
        # check_object_permissionsはgeneric.GenericAPIView内で呼ばれるので、
        # viewsets.ViewSetを直接継承する際はpremissionsがcheck_object_permissionsを
        # 持っていないか注意する。
        premissions = (
            permissions.IsAdminUser | getIsOrganizationAdmin(self.organization_pk),
        )
        return [permission() for permission in premissions]

    def _get_model(self):
        service = generics.get_object_or_404(Service.objects.all(), id=self.service_pk)

        organization_id = self.request.parser_context["kwargs"][self.organization_pk]
        organization = generics.get_object_or_404(
            Organization.objects.prefetch_related("services").all(), id=organization_id
        )
        return service, organization

    @action(methods=["post"], detail=True)
    def contract(self, request, *args, **kwargs):
        service, organization = self._get_model()

        services = organization.services.all()
        if services.filter(id=service.id).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        organization.services.add(service)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=True)
    def cancel(self, request, *args, **kwargs):
        service, organization = self._get_model()

        services = organization.services.all()
        if not services.filter(id=service.id).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        organization.services.remove(service)

        return Response(status=status.HTTP_204_NO_CONTENT)
