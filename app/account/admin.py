from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse

# Register your models here.



class InstagramInline(admin.StackedInline):
    model = Instagram
    max_num = 10
    extra = 1




User = get_user_model()

class UserAdmin(BaseUserAdmin):

    list_display = ('email', 'name', 'surname', 'is_active', 'is_superuser')
    list_filter = ('is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'surname')}),

        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','surname', 'password1', 'password2')}
        ),
    )
    readonly_fields = ('timestamp',)

    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)
    filter_horizontal = ()
    inlines = [InstagramInline]


admin.site.register(User, UserAdmin)
