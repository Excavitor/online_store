from django.shortcuts import render
from django.http import HttpResponse
from store_app.models import Customer, Category, Order, Product, OrderItem

# Create your views here.
# def home(request):
#     return HttpResponse("Hello, world. You're at the home page.")

def home(request):
    customer_orders_pending = Customer.objects.filter(order__status='Pending')


    return render(
        request,
        'index.html',
        {
            'name': 'Shad Abdullah',
            'customer_orders_pending': list(customer_orders_pending),
        }
    )
