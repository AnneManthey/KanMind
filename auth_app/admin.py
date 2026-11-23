"""Admin configuration for the custom user model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(AdminUserCreationForm):
    """Create a user in the admin with e-mail and full name."""

    class Meta:
        model = User
        fields = ("email", "fullname")


class CustomUserChangeForm(UserChangeForm):
    """Edit a user in the admin without the removed username field."""

    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin for the e-mail based user model."""

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    ordering = ("email",)
    list_display = ("email", "fullname", "is_staff")
    search_fields = ("email", "fullname")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("fullname",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "fullname",
                    "usable_password",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
