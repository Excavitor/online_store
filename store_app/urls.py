from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customers, name='customer'),
    path('orders/', views.orders, name='orders'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('orderitems/', views.orderitems, name='orderitems'),
]
