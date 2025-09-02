from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerificationToken, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_email_verified', 'country', 'is_staff', 'date_joined')
    list_filter = ('is_email_verified', 'country', 'preferred_study_level', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('profile_picture', 'date_of_birth', 'country', 'is_email_verified')
        }),
        ('Preferences', {
            'fields': ('preferred_study_level', 'preferred_fields', 'budget_min', 'budget_max')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile Information', {
            'fields': ('email', 'first_name', 'last_name')
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at')