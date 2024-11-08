from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

user_model = get_user_model()

@admin.register(user_model)
class CustomUserAdmin(UserAdmin):
    model = user_model
    list_display = ('email', 'is_superuser', 'is_active',)
    list_filter = ('email', 'is_superuser', 'is_active',)
    search_fields = ('email', )
    ordering = ('email', )
    fieldsets =(
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',)}),
        ('group permissions', {'fields': ('groups', 'user_permissions',)}),
        ('login', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
