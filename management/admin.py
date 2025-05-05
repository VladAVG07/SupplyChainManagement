from django.contrib import admin

# Register your models here.

from .models import *

class SuppliersProductsInline(admin.TabularInline):
    model = SupplierProducts
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [SuppliersProductsInline]

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 3

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]
    

admin.site.register(Suppliers)
admin.site.register(Products, ProductAdmin)


