from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import admin
from django.contrib.messages import info

from orders.models import Order, OrderImage, OrderPrice


class OrderImageInline(admin.TabularInline):
    model = OrderImage
    extra = 0
    max_num = 6


@admin.register(OrderPrice)
class OrderPriceAdmin(admin.ModelAdmin):
    list_display = ('order', 'cost_price', 'sale_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_make_model', 'status', 'created_at', 'updated_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    inlines = [OrderImageInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not hasattr(self, 'original_statuses'):
            self.original_statuses = {}
        self.original_statuses = {obj.id: obj.status for obj in queryset}
        return queryset

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST" and "_save" in request.POST:
            changed_orders = []
            original_statuses = {
                obj.id: obj.status for obj in self.get_queryset(request)
            }

            for key, value in request.POST.items():
                if key.startswith("form-") and key.endswith("-status"):
                    form_index = key.split("-")[1]
                    order_id_key = f"form-{form_index}-id"
                    order_id = request.POST.get(order_id_key)
                    if order_id:
                        try:
                            order_id = int(order_id)
                            original_status = original_statuses.get(order_id)
                            if original_status and original_status != value and value == "completed":
                                order = Order.objects.get(id=order_id)
                                if not hasattr(order, 'price'):
                                    changed_orders.append(order)
                        except (Order.DoesNotExist, ValueError):
                            pass

            if len(changed_orders) == 1:
                response = super().changelist_view(request, extra_context)
                order = changed_orders[0]
                url = reverse('admin:orders_orderprice_add') + f"?order={order.id}"
                return redirect(url)
            elif len(changed_orders) > 1:
                info(request, "Перенаправление невозможно: изменено несколько заказов.")

        return super().changelist_view(request, extra_context)
