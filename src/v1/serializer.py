from dataclasses import fields
from rest_framework import serializers
from account.models import Organization, Service, Membership, User


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class ServicesSerializer(serializers.ListSerializer):
    child = ServiceSerializer()


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"

    services = ServicesSerializer()


class OrganizationMemberSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "role")
        read_only_fields = ("email",)

    def get_role(self, obj):
        return obj.membership.role


class OrganizationMemberUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=[role[0] for role in Membership.ROLE], allow_null=True, required=False
    )


class OrganizationMemberCreateSerializer(OrganizationMemberUpdateSerializer):
    id = serializers.UUIDField(format="hex_verbose", required=True)


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class EmptySerializer(serializers.Serializer):
    pass
