from django.shortcuts import render, redirect, get_object_or_404
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
            'name': 'Shad Abdullah',
            'products_set': list(products_set),
        }
    )

def add_product(request):
    categories_set = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')
        category_id = request.POST.get('category')
        is_available = request.POST.get('is_available') == 'on'

        if title and price and inventory and category_id:
            category = Category.objects.get(id=category_id)
            Product.objects.create(
                title=title,
                description=description,
                price=price,
                inventory=inventory,
                category=category,
                is_available=is_available
            )
            return redirect('products')

    return render(
        request,
        'add_product.html',
        {'categories_set': categories_set, 'name': 'Shad Abdullah'}
    )

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories_set = Category.objects.all()

    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.inventory = request.POST.get('inventory')
        category_id = request.POST.get('category')
        product.is_available = request.POST.get('is_available') == 'on'

        if product.title and product.price and product.inventory and category_id:
            product.category = Category.objects.get(id=category_id)
            product.save()
            return redirect('products')

    return render(
        request,
        'edit_product.html',
        {
            'product': product,
            'categories_set': categories_set,
            'name': 'Shad Abdullah'
        }
    )

def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
    return redirect('products')


# def products(request):
#     sort_by = request.GET.get('sort_by', 'created_at')  # Default sort by 'created_at'
#     allowed_sort_fields = ['id', 'title', 'price', 'inventory', 'created_at',
#                            'category__title']  # Add valid fields for sorting
#
#     # Prepend '-' for descending order if the field is clicked again (more advanced, for now, simple sort)
#     # Basic validation: if sort_by parameter is not in allowed fields, default to 'created_at'
#     # For foreign key fields like category, use 'category__title' to sort by category title
#
#     actual_sort_field = sort_by
#     if sort_by.startswith('-'):
#         actual_sort_field = sort_by[1:]  # Get the field name without '-'
#
#     if actual_sort_field not in [field.replace('category__title', 'category') for field in
#                                  allowed_sort_fields]:  # Adjust for category check
#         sort_by = 'created_at'  # Default to a safe field
#
#     # Prevent sorting by description as it's a TextField and might not be efficient or meaningful
#     if 'description' in sort_by:
#         sort_by = 'created_at'
#
#     try:
#         products_set = Product.objects.all().order_by(sort_by)
#     except Exception as e:  # Catch potential errors if sort_by is invalid despite checks
#         products_set = Product.objects.all().order_by('created_at')
#
#     return render(
#         request,
#         'products.html',
#         {
#             'products_set': list(products_set),
#             'current_sort': sort_by,  # Pass current sort to template for link generation
#             'name': 'Shad Abdullah',  # Assuming 'name' is still needed in this template
#         }
#     )

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
