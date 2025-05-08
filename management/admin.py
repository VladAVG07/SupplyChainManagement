from django.contrib import admin
from geopy.geocoders import Nominatim
from .forms import WarehouseAdminForm

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
    readonly_fields = ('latitude', 'longitude')
    pass

@admin.register(SupplierProducts)
class SupplierProductsAdmin(AutoListDisplayAdmin):
    pass

@admin.register(Suppliers)
class SuppliersAdmin(AutoListDisplayAdmin):
    pass

@admin.register(Warehouses)
class WarehouseAdmin(admin.ModelAdmin):
    form = WarehouseAdminForm  # Use the custom form
    list_display = ('warehouse_id', 'name', 'lat', 'long')  # Display fields in the admin list view
    fields = ('name', 'capacity', 'lat', 'long', 'address')  # Include the custom 'address' field in the form
    readonly_fields = ('lat', 'long')  # Make latitude and longitude read-only

    def save_model(self, request, obj, form, change):
        address = form.cleaned_data.get('address')  # Get the address from the form
        if address:  # Check if the address field is filled
            geolocator = Nominatim(user_agent="warehouse_geocoder")
            location = geolocator.geocode(address)
            if location:
                obj.lat = location.latitude
                obj.long = location.longitude
        super().save_model(request, obj, form, change)


