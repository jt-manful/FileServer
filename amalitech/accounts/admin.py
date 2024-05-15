from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FileServerUser

class FileServerUserAdmin(UserAdmin):
    model = FileServerUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )

admin.site.register(FileServerUser, FileServerUserAdmin)

