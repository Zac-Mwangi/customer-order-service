from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions, response

from django.contrib.auth import authenticate

from rest_framework.decorators import api_view

from .models import Customer as User
from rest_framework.permissions import IsAuthenticated


# get logged in user
class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({"user": serializer.data})


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    # bypass authentication
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()  # make sure the serializer implements the create method
            return Response(
                {
                    "success": True,
                    "message": "Resource created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Invalid data.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    authentication_classes = []

    def post(self, request):
        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)

        # Check if email or password is missing
        if not email or not password:
            return Response(
                {
                    "success": False,
                    "message": "Email and password are required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=email, password=password)

        # Check if authentication failed
        if not user:
            return Response(
                {
                    "success": False,
                    "message": "Invalid credentials, please try again.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.serializer_class(user)

        return Response(
            {
                "success": True,
                "message": "Request processed successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {"success": False, "message": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = UserSerializer(user)  # Replace with your serializer
    return Response(
        {
            "success": True,
            "message": "User retrieved successfully.",
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
