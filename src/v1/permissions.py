from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from account.models import Membership


def getIsOrganizationMember(organization_pk):
    class IsOrganizationMember(permissions.BasePermission):
        def has_permission(self, request, view):
            if isinstance(request.user, AnonymousUser):
                return False
            try:
                membership = Membership.objects.prefetch_related(
                    "user", "organization"
                ).get(user=request.user.id)
                return (
                    str(membership.organization.id)
                    == request.parser_context["kwargs"][organization_pk]
                )
            except:
                return False

    return IsOrganizationMember


def getIsOrganizationAdmin(organization_pk):
    class IsOrganizationAdmin(permissions.BasePermission):
        def has_permission(self, request, view):
            print(1111, request.parser_context["kwargs"])
            if isinstance(request.user, AnonymousUser):
                return False
            try:
                membership = Membership.objects.prefetch_related(
                    "user", "organization"
                ).get(user=request.user.id)
                return (
                    str(membership.organization.id)
                    == request.parser_context["kwargs"][organization_pk]
                    and membership.role == "admin"
                )
            except:
                return False

    return IsOrganizationAdmin


def getIsUserSelf(user_pk):
    class IsUserSelf(permissions.BasePermission):
        def has_permission(self, request, view):
            if isinstance(request.user, AnonymousUser):
                return False

            return str(request.user.id) == request.parser_context["kwargs"][user_pk]

    return IsUserSelf
