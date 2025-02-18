# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("phone_number", "full_name", "telegram_id", "is_staff", "is_active")
    list_filter = ("phone_number", "full_name", "telegram_id", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "password1", "password2", "is_admin", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("phone_number",)
    ordering = ("phone_number",)

admin.site.register(CustomUser, CustomUserAdmin)


# Customizing the Admin site headers
admin.site.site_header = "SFX Administration"
admin.site.site_title = "SFX Admin Portal"
admin.site.index_title = "Welcome to the SFX Admin Dashboard"

admin.site.unregister(Group)