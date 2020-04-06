from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from shop.models import Color, Product, Size, Order, OrderItem, Review, Tracking, TrackingItem

class ExportModel(ImportExportModelAdmin):
  pass

admin.site.register(Product, ExportModel)
admin.site.register(Size, ExportModel)
admin.site.register(Color, ExportModel)
admin.site.register(OrderItem, ExportModel)
admin.site.register(Order, ExportModel)
admin.site.register(Review, ExportModel)
admin.site.register(Tracking, ExportModel)
admin.site.register(TrackingItem, ExportModel)
