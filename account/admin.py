from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from import_export.admin import ImportExportModelAdmin
from jalali_date.admin import ModelAdminJalaliMixin




class UserAdminChange(ImportExportModelAdmin,ModelAdminJalaliMixin,admin.ModelAdmin):

    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'special_user',
        'is_superuser',
        'is_staff',
        'is_author',
        'groups',
        'user_permissions','photo'

    )

    list_display = ('username','email','is_staff','is_author','is_special_user')
    search_fields  = ('username','email')
    list_filter = ('username','email')
    list_per_page = 10


admin.site.register(User,UserAdminChange)