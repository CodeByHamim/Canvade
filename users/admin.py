from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser


def assign_role(user):
    try:
        role = user.role.lower()
        group, _ = Group.objects.get_or_create(name=role)  # auto-create if missing
        user.groups.clear()  # remove from any previous groups
        user.groups.add(group)
    except Group.DoesNotExist:
        pass  # optionally log error


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Automatically assign group when a user is created via admin
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        assign_role(obj)
