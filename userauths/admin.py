from django.contrib import admin
from .models import Profile, User
from import_export.admin import ImportExportModelAdmin

class UserAdmin(ImportExportModelAdmin):
    pass

class ProfileAdmin(ImportExportModelAdmin):
    list_display = ['user']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)