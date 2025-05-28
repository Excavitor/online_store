from django.contrib import admin

from store_app.models import Customer, Order, OrderItem, Product, Category


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'created_at']
    list_per_page = 5

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'price', 'inventory', 'is_available', 'created_at']
    list_editable = ['is_available', 'price']
    list_filter = ['is_available', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'status']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'unit_price']


