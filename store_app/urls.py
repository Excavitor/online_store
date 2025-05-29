from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customers, name='customer'),
    path('orders/', views.orders, name='orders'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orderitems/', views.orderitems, name='orderitems'),
]
