from django.shortcuts import render
from django.http import HttpResponse
from store_app.models import Customer, Category, Order, Product, OrderItem

# Create your views here.
# def home(request):
#     return HttpResponse("Hello, world. You're at the home page.")

def dashboard(request):
    customer_orders_pending = Customer.objects.filter(order__status='Pending')


    return render(
        request,
        'dashboard.html',
        {
            'name': 'Shad Abdullah',
            'customer_orders_pending': list(customer_orders_pending),
        }
    )

def customers(request):
    customers_set = Customer.objects.all()
    return render(
        request,
        'customers.html',
        {
            'customers_set': list(customers_set),
        }
    )

def products(request):
    products_set = Product.objects.all()
    return render(
        request,
        'products.html',
        {
            'products_set': list(products_set),
        }
    )

def orders(request):
    orders_set = Order.objects.all()
    return render(
        request,
        'orders.html',
        {
            'orders_set': list(orders_set),
        }
    )

def orderitems(request):
    orderitems_set = OrderItem.objects.all()
    return render(
        request,
        'orderitems.html',
        {
            'orderitems_set': list(orderitems_set),
        }
    )

def categories(request):
    categories_set = Category.objects.all()
    return render(
        request,
        'categories.html',
        {
            'categories_set': list(categories_set),
        }
    )
