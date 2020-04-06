from django.contrib import admin
from nugs.models import Bloc, Member
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ExportModel(ImportExportModelAdmin):
  pass

admin.site.register(Bloc, ExportModel)
admin.site.register(Member, ExportModel)