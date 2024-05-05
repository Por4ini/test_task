from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_verified', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_verified', 'groups', 'user_permissions')}
        ),
    )
    list_display = ('email', 'username', 'phone', 'is_active', 'is_staff', 'is_verified')
    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
