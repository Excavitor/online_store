from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['-created_at']

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default="-")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Product Categories"

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices= STATUS_CHOICES,  default="Pending")

    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name

    class Meta:
        ordering = ['status', 'placed_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.product.title

    class Meta:
        ordering = ['-quantity', '-unit_price']