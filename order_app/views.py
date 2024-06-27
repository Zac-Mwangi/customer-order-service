from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Order, Customer
from .serializers import OrderSerializer
from .functions import sms_service
from django.db.models import Q


@api_view(["GET"])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(
        {
            "success": True,
            "message": "Retrieve Successful",
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def retrieve_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(
            {
                "success": True,
                "message": "Retrieve Successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Order not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
def create_order(request):
    request.data["customer"] = request.user.id

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        # Fetch the customer's phone number

        order = serializer.save()
        customer = Customer.objects.get(id=request.user.id)
        phone_number = customer.phone_number
        message = f"Dear {customer.username}, your order for {order.item} has been successfully created."
        sms_service.send(message, phone_number)

        return Response(
            {
                "success": True,
                "message": "Order created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "success": False,
            "message": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["PUT"])
def update_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Order not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Updated Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    return Response(
        {
            "success": False,
            "message": "Invalid data provided.",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(
            {
                "success": True,
                "message": "Deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Order not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
def retrieve_orders_by_customer(request, customer_id):
    try:
        orders = Order.objects.filter(
            customer__id=customer_id,
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(
            {
                "success": True,
                "message": "Retrieve Successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Orders not found for this customer.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
