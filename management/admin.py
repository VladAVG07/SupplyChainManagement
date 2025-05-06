from django.contrib import admin

# Register your models here.

from .models import *

class AutoListDisplayAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # Dynamically set list_display to include all fields of the model
        self.list_display = [field.name for field in model._meta.fields]

class SuppliersProductsInline(admin.TabularInline):
    model = SupplierProducts
    extra = 1

@admin.register(Products)
class ProductAdmin(AutoListDisplayAdmin):
    inlines = [SuppliersProductsInline]

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1

@admin.register(Orders)
class OrderAdmin(AutoListDisplayAdmin):
    inlines = [OrderItemsInline]  # You can still add custom behavior like inlines

@admin.register(Customers)
class CustomersAdmin(AutoListDisplayAdmin):
    pass

@admin.register(Inventory)
class InventoryAdmin(AutoListDisplayAdmin):
    pass

@admin.register(OrderItems)
class OrderItemsAdmin(AutoListDisplayAdmin):
    pass

@admin.register(Payments)
class PaymentsAdmin(AutoListDisplayAdmin):
    pass

@admin.register(Shipments)
class ShipmentsAdmin(AutoListDisplayAdmin):
    pass

@admin.register(SupplierProducts)
class SupplierProductsAdmin(AutoListDisplayAdmin):
    pass

@admin.register(Suppliers)
class SuppliersAdmin(AutoListDisplayAdmin):
    pass

@admin.register(Warehouses)
class WarehouseAdmin(AutoListDisplayAdmin):
    pass


