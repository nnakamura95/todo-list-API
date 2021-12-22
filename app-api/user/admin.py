from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    ordering = ('-date_joined', )
    list_filter = ['last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'date_joined', 'is_active', 'is_active', 'is_superuser'
    ]
    fieldsets = (
        ('Basic Information', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
