from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'address',
                    'postal_code', 'has_paid', 'created')
    list_display_links = ('id', 'created')
    list_filter = ('has_paid', 'created')
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)

# Register your models here.
