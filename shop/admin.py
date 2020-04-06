from django.contrib import admin

# Register your models here.
from shop.models import Color, Product, Size, Order, OrderItem, Review, Tracking, TrackingItem

admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Tracking)
admin.site.register(TrackingItem)
