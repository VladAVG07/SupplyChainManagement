# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'customers'


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class OrderItems(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    CHOICES = [(status, status) for status in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Canceled']]

    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True, choices=CHOICES)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.order_id) + ' - ' + self.customer.name 

    class Meta:
        managed = False
        db_table = 'orders'


class Payments(models.Model):
    CHOICES = [(status, status) for status in ['Pending', 'Completed', 'Failed', 'Refunded']]
    CHOICES2 = [(status, status) for status in ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash']]

    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True, choices=CHOICES2)
    status = models.CharField(max_length=50, blank=True, null=True, choices=CHOICES)

    class Meta:
        managed = False
        db_table = 'payments'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.product_id) + ' - ' + self.name

    class Meta:
        managed = False
        db_table = 'products'


class Shipments(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    delivery_status = models.CharField(max_length=50, blank=True, null=True)
    tracking_number = models.CharField(unique=True, max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)


    class Meta:
        managed = False
        db_table = 'shipments'


class SupplierProducts(models.Model):
    supplier = models.OneToOneField('Suppliers', models.DO_NOTHING, primary_key=True)  # The composite primary key (supplier_id, product_id) found, that is not supported. The first column is selected.
    product = models.ForeignKey(Products, models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'supplier_products'
        unique_together = (('supplier', 'product'),)


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.supplier_id) + ' - ' + self.name
    

    class Meta:
        managed = False
        db_table = 'suppliers'


class Warehouses(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    long = models.DecimalField(max_digits=20, decimal_places=15)

    def __str__(self):
        return str(self.warehouse_id) + ' - ' + self.name

    class Meta:
        managed = False
        db_table = 'warehouses'
