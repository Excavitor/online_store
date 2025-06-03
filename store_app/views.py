from django.db.models import Sum
from django.shortcuts import render, redirect
# Make sure to import your models at the top
from .models import Category, Product, Customer, Order, OrderItem  # Added Category and Product
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, UserEditForm, RoleForm
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import get_object_or_404


# Updated home view
def home(request):
    categories_set = Category.objects.all()

    # Fetch some products - you can customize these queries
    # For example, featured electronics (assuming a category named 'Electronics')
    try:
        electronics_category = Category.objects.get(title__iexact='Electronics')
        featured_electronics = Product.objects.filter(category=electronics_category, is_available=True)[:5]
    except Category.DoesNotExist:
        featured_electronics = Product.objects.none()  # Empty queryset if category doesn't exist

    # For example, bestselling books (assuming a category named 'Books')
    try:
        books_category = Category.objects.get(title__iexact='Books')
        bestselling_books = Product.objects.filter(category=books_category, is_available=True)[
                            :3]  # Show 3 bestselling books
    except Category.DoesNotExist:
        bestselling_books = Product.objects.none()  # Empty queryset

    most_ordered_products = Product.objects.annotate(
        total_ordered_quantity=Sum('orderitem__quantity')
    ).filter(
        total_ordered_quantity__gt=0
    ).order_by(
        '-total_ordered_quantity'
    )[:5]  # Get top 5 most ordered products, you can change this number

    context = {
        'categories_set': categories_set,
        # 'featured_electronics': featured_electronics,
        # 'bestselling_books': bestselling_books,
        'most_ordered_products': most_ordered_products,
    }
    return render(request, 'store_app/home.html', context)


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
    return render(request, 'store_app/user_form.html',
                  {'form': form, 'user_obj': user, 'action': 'Edit', 'name': 'Shad Abdullah'})


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
    return render(request, 'store_app/role_form.html',
                  {'form': form, 'role_obj': role, 'action': 'Edit', 'name': 'Shad Abdullah'})


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
            'name': 'Shad Abdullah'  # Added name here
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
    orders_set = Order.objects.select_related('customer').all()  # Optimized query
    # No need to manually add customer_name if you access it via order_item.customer.first_name in template
    return render(
        request,
        'orders.html',
        {
            'orders_set': orders_set,  # No need to convert to list here
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
                messages.success(request, "Order added successfully!")
                return redirect('orders')
            except Customer.DoesNotExist:
                messages.error(request, "Selected customer not found.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Status and Customer are required.")

    context = {
        'customers_set': customers_set,
        'name': 'Shad Abdullah',
        'status_choices': status_choices
    }
    return render(request, 'add_order.html', context)


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customers_set = Customer.objects.all()
    status_choices = Order.STATUS_CHOICES

    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_customer_id = request.POST.get('customer_id')

        if new_status and new_customer_id:
            try:
                customer_instance = Customer.objects.get(id=new_customer_id)
                order.status = new_status
                order.customer = customer_instance
                order.save()
                messages.success(request, f"Order ID: {order.id} updated successfully!")
                return redirect('orders')
            except Customer.DoesNotExist:
                messages.error(request, "Selected customer not found.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Status and Customer are required.")

    context = {
        'order': order,
        'customers_set': customers_set,
        'status_choices': status_choices,
        'name': 'Shad Abdullah'
    }
    return render(request, 'edit_order.html', context)


def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order_id_display = order.id
        order.delete()
        messages.success(request, f"Order ID: {order_id_display} deleted successfully.")
    return redirect('orders')


def orderitems(request):
    orderitems_set = OrderItem.objects.select_related('order__customer', 'product').all()
    context = {
        'orderitems_set': orderitems_set,
        'name': 'Shad Abdullah'
    }
    return render(request, 'orderitems.html', context)


def add_order_item(request):
    orders = Order.objects.select_related('customer').all()
    products_qs = Product.objects.filter(is_available=True)  # Renamed to avoid conflict

    if request.method == 'POST':
        order_id = request.POST.get('order')
        product_id = request.POST.get('product')
        quantity_str = request.POST.get('quantity')
        unit_price_str = request.POST.get('unit_price')

        if order_id and product_id and quantity_str and unit_price_str:
            try:
                order = Order.objects.get(id=order_id)
                product_instance = Product.objects.get(id=product_id)  # Renamed
                quantity = int(quantity_str)
                unit_price = Decimal(unit_price_str)

                if quantity < 1:
                    messages.error(request, "Quantity must be at least 1.")
                else:
                    OrderItem.objects.create(
                        order=order,
                        product=product_instance,  # Use renamed variable
                        quantity=quantity,
                        unit_price=unit_price
                    )
                    messages.success(request, "Order item added successfully!")
                    return redirect('orderitems')
            except Order.DoesNotExist:
                messages.error(request, "Selected order not found.")
            except Product.DoesNotExist:
                messages.error(request, "Selected product not found.")
            except ValueError:
                messages.error(request, "Invalid quantity or unit price format.")
        else:
            messages.error(request, "All fields are required.")

    context = {
        'orders': orders,
        'products': products_qs,  # Use renamed variable
        'name': 'Shad Abdullah'
    }
    return render(request, 'add_order_item.html', context)


def edit_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    products_qs = Product.objects.filter(is_available=True)  # Renamed

    if request.method == 'POST':
        quantity_str = request.POST.get('quantity')
        unit_price_str = request.POST.get('unit_price')
        product_id_str = request.POST.get('product')

        if quantity_str and unit_price_str and product_id_str:
            try:
                quantity = int(quantity_str)
                unit_price = Decimal(unit_price_str)
                product_instance = Product.objects.get(id=product_id_str)  # Renamed

                if quantity < 1:
                    messages.error(request, "Quantity must be at least 1.")
                else:
                    order_item.product = product_instance  # Use renamed
                    order_item.quantity = quantity
                    order_item.unit_price = unit_price
                    order_item.save()
                    messages.success(request, "Order item updated successfully!")
                    return redirect('orderitems')
            except Product.DoesNotExist:
                messages.error(request, "Selected product not found.")
            except ValueError:
                messages.error(request, "Invalid quantity or unit price format.")
        else:
            messages.error(request, "Quantity, Unit Price, and Product are required.")

    context = {
        'order_item': order_item,
        'products': products_qs,  # Use renamed
        'name': 'Shad Abdullah'
    }
    return render(request, 'edit_order_item.html', context)


def delete_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    if request.method == 'POST':
        order_item_repr = f"Item '{order_item.product.title}' from Order ID {order_item.order.id}"
        order_item.delete()
        messages.success(request, f"{order_item_repr} deleted successfully.")
    return redirect('orderitems')


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
        slug = request.POST.get('slug')

        if title and slug:
            if Category.objects.filter(slug=slug).exists():
                messages.error(request, f"A category with slug '{slug}' already exists.")
            else:
                Category.objects.create(title=title, slug=slug)
                messages.success(request, f"Category '{title}' created successfully!")
                return redirect('categories')
        else:
            messages.error(request, "Title and slug are required.")

    return render(
        request,
        'add_category.html',
        {'name': 'Shad Abdullah'}
    )


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')

        if title and slug:
            # Check if slug is being changed and if the new one conflicts
            if category.slug != slug and Category.objects.filter(slug=slug).exclude(id=category_id).exists():
                messages.error(request, f"Another category with slug '{slug}' already exists.")
            else:
                category.title = title
                category.slug = slug
                category.save()
                messages.success(request, f"Category '{category.title}' updated successfully!")
                return redirect('categories')
        else:
            messages.error(request, "Title and slug are required.")

    return render(
        request,
        'edit_category.html',
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
            messages.success(request, f"Category '{category_title}' deleted successfully.")
        except Exception as e:
            messages.error(request, f"Could not delete category '{category.title}'. It might be in use. Details: {e}")
    return redirect('categories')