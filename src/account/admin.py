from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User, Organization, Service, Membership


class MembershipInline(admin.StackedInline):
    model = Membership
    verbose_name = "所属"


class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("email", "password", "last_login")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    readonly_fields = ("last_login",)

    list_display = (
        "email",
        "is_staff",
    )
    list_filter = ("is_superuser", "is_active")
    search_fields = ("email", "email")
    ordering = ("email",)
    inlines = [MembershipInline]


admin.site.register(Service)
admin.site.register(Organization)
admin.site.register(User, CustomUserAdmin)

admin.site.unregister(Group)
