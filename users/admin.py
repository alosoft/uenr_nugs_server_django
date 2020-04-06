from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
#
# # Register your models here.
from users.models import User

class UserAdmin(ImportExportModelAdmin):
  pass
admin.site.register(User, UserAdmin)
