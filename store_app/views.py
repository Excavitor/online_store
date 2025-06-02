from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store_app.models import Customer, Category, Order, Product, OrderItem

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required # Optional: if you want to protect these views
from .forms import UserCreationForm, UserEditForm, RoleForm # Import your new forms
from django.contrib import messages # For showing success/error messages
from decimal import Decimal

# Create your views here.
# def home(request):
#     return HttpResponse("Hello, world. You're at the home page.")

def home(request):
    return render(request, 'store_app/home.html')

def list_users(request):
    users = User.objects.all()
    return render(request, 'store_app/users_list.html', {'users_set': users, 'name': 'Shad Abdullah'})

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User '{user.username}' created successfully!")
            return redirect('list_users')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'store_app/user_form.html', {'form': form, 'action': 'Create', 'name': 'Shad Abdullah'})

# @login_required (optional)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user.username}' updated successfully!")
            return redirect('list_users')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserEditForm(instance=user)
    return render(request, 'store_app/user_form.html', {'form': form, 'user_obj': user, 'action': 'Edit', 'name': 'Shad Abdullah'})

# @login_required (optional)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if request.user.id == user.id:
             messages.error(request, "You cannot delete yourself.")
             return redirect('list_users')
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully.")
        return redirect('list_users')
    # return render(request, 'store_app/user_confirm_delete.html', {'user_obj': user, 'name': 'Shad Abdullah'})
    return redirect('list_users')

def list_roles(request):
    roles = Group.objects.all()
    return render(request, 'store_app/roles_list.html', {'roles_set': roles, 'name': 'Shad Abdullah'})

def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            messages.success(request, f"Role '{role.name}' created successfully!")
            return redirect('list_roles')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RoleForm()
    return render(request, 'store_app/role_form.html', {'form': form, 'action': 'Create', 'name': 'Shad Abdullah'})

# @login_required (optional)
def edit_role(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, f"Role '{role.name}' updated successfully!")
            return redirect('list_roles')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RoleForm(instance=role)
    return render(request, 'store_app/role_form.html', {'form': form, 'role_obj': role, 'action': 'Edit', 'name': 'Shad Abdullah'})

# @login_required (optional)
def delete_role(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    if request.method == 'POST':
        role_name = role.name
        if role.user_set.exists():
             messages.error(request, f"Role '{role_name}' is in use and cannot be deleted.")
             return redirect('list_roles')
        role.delete()
        messages.success(request, f"Role '{role_name}' deleted successfully.")
        return redirect('list_roles')
    # return render(request, 'store_app/role_confirm_delete.html', {'role_obj': role, 'name': 'Shad Abdullah'})
    return redirect('list_roles')

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


def orders(request):
    orders_set = Order.objects.all()
    for o in orders_set:
        o.customer_name = f"{o.customer.first_name} {o.customer.last_name}"

    return render(
        request,
        'orders.html',
        {
            'orders_set': list(orders_set),
            'name': 'Shad Abdullah'
        }
    )


def add_order(request):
    customers_set = Customer.objects.all()
    status_choices = Order.STATUS_CHOICES

    if request.method == 'POST':
        status = request.POST.get('status')
        customer_id = request.POST.get('customer_id')

        if status and customer_id:
            try:
                customer_instance = Customer.objects.get(id=customer_id)
                Order.objects.create(
                    customer=customer_instance,
                    status=status
                )
                return redirect('orders')
            except Customer.DoesNotExist:
                # Handle error: Customer not found
                # You might want to add a message here using Django's messages framework
                pass
            except Exception as e:
                # Handle other potential errors
                pass
        else:
            # Handle error: Missing fields
            pass

    context = {
        'customers_set': customers_set,
        'name': 'Shad Abdullah',
        'status_choices': status_choices
    }
    return render(request, 'add_order.html', context)


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customers_set = Customer.objects.all()
    status_choices = Order.STATUS_CHOICES # Pass status choices

    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_customer_id = request.POST.get('customer_id')

        if new_status and new_customer_id:
            try:
                customer_instance = Customer.objects.get(id=new_customer_id)
                order.status = new_status
                order.customer = customer_instance
                order.save()
                return redirect('orders')
            except Customer.DoesNotExist:
                # Add error handling/message
                pass
            # Add other error handling as needed
        else:
            # Add error handling for missing fields
            pass

    context = {
        'order': order,
        'customers_set': customers_set,
        'status_choices': status_choices, # Add to context
        'name': 'Shad Abdullah' # Or however you get the admin name
    }
    return render(request, 'edit_order.html', context)

def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.delete()
    return redirect('orders')


def orderitems(request):
    orderitems_set = OrderItem.objects.all()

    # Calculate total price for each item
    # for item in orderitems_set:
        # item.total_price = item.quantity * item.unit_price
        # In Python, multiplying an int (quantity) by a Decimal (unit_price)
        # correctly results in a Decimal, which is what we want.

    context = {
        'orderitems_set': orderitems_set,  # No need to convert to list here if iterating in template
        'name': 'Shad Abdullah'  # Assuming this is still needed
    }
    return render(request, 'orderitems.html', context)

# def orderitems(request):
#     orderitems_set = OrderItem.objects.all()
#     return render(
#         request,
#         'orderitems.html',
#         {
#             'orderitems_set': list(orderitems_set),
#         }
#     )


def add_order_item(request):
    orders = Order.objects.all()  # To select an order
    products = Product.objects.all()  # To select a product

    if request.method == 'POST':
        order_id = request.POST.get('order')
        product_id = request.POST.get('product')
        quantity_str = request.POST.get('quantity')
        unit_price_str = request.POST.get('unit_price')  # Price at the time of adding

        if order_id and product_id and quantity_str and unit_price_str:
            try:
                order = Order.objects.get(id=order_id)
                product = Product.objects.get(id=product_id)
                quantity = int(quantity_str)
                unit_price = Decimal(unit_price_str)

                if quantity < 1:
                    # messages.error(request, "Quantity must be at least 1.")
                    pass  # Add proper error handling
                else:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price
                    )
                    # messages.success(request, "Order item added successfully!")
                    return redirect('orderitems')  # Or redirect to the specific order's detail page
            except Order.DoesNotExist:
                # messages.error(request, "Selected order not found.")
                pass
            except Product.DoesNotExist:
                # messages.error(request, "Selected product not found.")
                pass
            except ValueError:  # For int/Decimal conversion
                # messages.error(request, "Invalid quantity or unit price format.")
                pass
        else:
            # messages.error(request, "All fields are required.")
            pass

    # For GET request or if POST fails, prepare context for the form
    # If you want to pre-fill unit_price based on product selection via JavaScript, that's an enhancement
    context = {
        'orders': orders,
        'products': products,
        'name': 'Shad Abdullah'
    }
    return render(request, 'add_order_item.html', context)


def edit_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    # Typically, you might not change the order or product of an existing order item.
    # If you do, you'll need to provide 'orders' and 'products' in the context for dropdowns.
    # For this example, we'll focus on quantity and unit_price.

    products = Product.objects.all()  # If you want to allow changing the product

    if request.method == 'POST':
        quantity_str = request.POST.get('quantity')
        unit_price_str = request.POST.get('unit_price')
        product_id_str = request.POST.get('product')  # If product is editable

        if quantity_str and unit_price_str and product_id_str:  # Add other validations as needed
            try:
                quantity = int(quantity_str)
                unit_price = Decimal(unit_price_str)
                product = Product.objects.get(id=product_id_str)

                if quantity < 1:
                    # messages.error(request, "Quantity must be at least 1.")
                    pass
                else:
                    order_item.product = product  # Update product if changed
                    order_item.quantity = quantity
                    order_item.unit_price = unit_price
                    order_item.save()
                    # messages.success(request, "Order item updated successfully!")
                    return redirect('orderitems')
            except Product.DoesNotExist:
                # messages.error(request, "Selected product not found.")
                pass
            except ValueError:
                # messages.error(request, "Invalid quantity or unit price format.")
                pass
        else:
            # messages.error(request, "Quantity, Unit Price, and Product are required.")
            pass

    context = {
        'order_item': order_item,
        'products': products,  # Pass products for the dropdown
        'name': 'Shad Abdullah'
    }
    return render(request, 'edit_order_item.html', context)


def delete_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    if request.method == 'POST':
        # order_item_repr = f"Item '{order_item.product.title}' from Order ID {order_item.order.id}"
        order_item.delete()
        # messages.success(request, f"{order_item_repr} deleted successfully.")
    return redirect('orderitems')  # Or redirect to the specific order's detail page

def categories(request):
    categories_set = Category.objects.all()
    return render(
        request,
        'categories.html',
        {
            'name': 'Shad Abdullah',
            'categories_set': list(categories_set),
        }
    )

def add_category(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug') # Assuming manual slug input for now

        # Basic validation: title and slug are required
        if title and slug:
            # Optional: Auto-generate slug if not provided or to ensure uniqueness
            # if not slug:
            #     slug = slugify(title)
            # Check for slug uniqueness if you're concerned about IntegrityError
            # if Category.objects.filter(slug=slug).exists():
            #     # Handle error: slug already exists
            #     # messages.error(request, f"A category with slug '{slug}' already exists.")
            #     pass # Add error handling
            # else:
            Category.objects.create(title=title, slug=slug)
            # messages.success(request, f"Category '{title}' created successfully!")
            return redirect('categories') # Redirect to the list of categories
        else:
            # Handle error: missing fields
            # messages.error(request, "Title and slug are required.")
            pass # Add error handling

    return render(
        request,
        'add_category.html', # You'll need to create this template
        {'name': 'Shad Abdullah'} # Pass any other context needed
    )

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')

        if title and slug:
            category.title = title
            category.slug = slug
            # Add uniqueness check for slug if necessary, excluding the current category instance
            # if Category.objects.filter(slug=slug).exclude(id=category_id).exists():
            #     # messages.error(request, f"Another category with slug '{slug}' already exists.")
            #     pass # Add error handling
            # else:
            category.save()
            # messages.success(request, f"Category '{category.title}' updated successfully!")
            return redirect('categories')
        else:
            # messages.error(request, "Title and slug are required.")
            pass # Add error handling

    return render(
        request,
        'edit_category.html', # You'll need to create this template
        {
            'category': category,
            'name': 'Shad Abdullah'
        }
    )

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        try:
            category_title = category.title
            category.delete()
            # messages.success(request, f"Category '{category_title}' deleted successfully.")
        except Exception as e: # For example, if protected by on_delete=PROTECT and there are related products
            # messages.error(request, f"Could not delete category '{category.title}'. Reason: {e}")
            pass # Add proper error handling
    return redirect('categories')