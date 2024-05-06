from dataclasses import fields
from rest_framework import serializers
from account.models import Organization, Service, Membership, User

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__' 


class ServicesSerializer(serializers.ListSerializer):
    child = ServiceSerializer()


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__' 

    services = ServicesSerializer()


class OrganizationMemberSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'role')

    def get_role(self, obj):
        return obj.membership.role


