from django.contrib import admin

from orders.models import Order, OrderImage


class PhotoInline(admin.TabularInline):
    model = OrderImage
    extra = 0
    max_num = 6


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']
    inlines = [PhotoInline]

