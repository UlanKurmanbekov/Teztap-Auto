from django.contrib import admin

from orders.models import Order, OrderImage


class OrderImageInline(admin.TabularInline):
    model = OrderImage
    extra = 0
    max_num = 6


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_make_model', 'status', 'created_at', 'updated_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    inlines = [OrderImageInline]

