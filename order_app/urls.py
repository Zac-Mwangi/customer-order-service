from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order-list'),  # GET all orders
    path('<int:pk>/', views.retrieve_order, name='order-detail'),  # GET a specific order
    path('create/', views.create_order, name='order-create'),  # POST create a new order
    path('update/<int:pk>/', views.update_order, name='order-update'),  # PUT update a specific order
    path('delete/<int:pk>/', views.delete_order, name='order-delete'),  # DELETE a specific order
    path('customer/<int:customer_id>/', views.retrieve_orders_by_customer, name='retrieve-orders-by-customer'),  # GET CUSTOMERS ORDER
]
