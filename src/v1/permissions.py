from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from account.models import Membership

class IsOrganizationMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        try:
            membership = Membership.objects.prefetch_related('user', 'organization').get(user=request.user.id)
            return str(membership.organization.id) == request.parser_context['kwargs']['organization_id']
        except:
            return False
        
class IsOrganizationAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser): 
            return False
        try:
            membership = Membership.objects.prefetch_related('user', 'organization').get(user=request.user.id)
            return str(membership.organization.id) == request.parser_context['kwargs']['organization_id'] and membership.role == 'admin'
        except:
            return False

class IsUserSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser): 
            return False
      
        return str(request.user.id) == request.parser_context['kwargs']['user_id']