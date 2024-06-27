from django.urls import path, include

urlpatterns = [
    path("customer/", include("customer_app.urls")),
    path("orders/", include("order_app.urls")),
]
