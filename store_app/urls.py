from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('customers/', views.customers, name='customer'),

    path('orders/', views.orders, name='orders'),
    path('orders/add/', views.add_order, name='add_order'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),

    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    path('products/', views.products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('orderitems/', views.orderitems, name='orderitems'),
    path('orderitems/add/', views.add_order_item, name='add_order_item'),
    path('orderitems/edit/<int:order_item_id>/', views.edit_order_item, name='edit_order_item'),
    path('orderitems/delete/<int:order_item_id>/', views.delete_order_item, name='delete_order_item'),

    path('users/', views.list_users, name='list_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path('roles/', views.list_roles, name='list_roles'),
    path('roles/create/', views.create_role, name='create_role'),
    path('roles/edit/<int:role_id>/', views.edit_role, name='edit_role'),
    path('roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),
]
