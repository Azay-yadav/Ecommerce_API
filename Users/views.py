from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
import requests
from Users.models import User
from Orders.models import Order
from ecomAPP.permissions import IsAdminUser, IsCustomerUser
from Orders.serializers import OrderSerializer
from .models import has_permission
from rest_framework.permissions import IsAuthenticated 
from .serializers import (
    RegisterSerializer,
    UserSerializer, UpdateUserSerializer, VerifyOTPSerializer
)


# USER REGISTRATION
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: "User registered successfully"})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "msg": "User registered successfully. Please check your email for OTP to verify your account.",
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# VERIFY OTP VIEW
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=VerifyOTPSerializer, responses={200: "Account verified successfully"})
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = get_object_or_404(User, email=email)

        if user.verification_code == otp:
            user.is_active = True
            user.is_verified = True
            user.verification_code = ''
            user.save()
            return Response({"msg": "Account verified successfully!"}, status=200)
        return Response({"error": "Invalid OTP"}, status=400)


# LOGOUT VIEW
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"msg": "Logged out successfully (JWT tokens are stateless)"}, status=status.HTTP_200_OK)


class UserOrderListView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# USER MANAGEMENT (Admin only)
class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrderUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
#check permissions
class CheckPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example: check if the user can 'view' 'product'
        can_view_product = has_permission(request.user, 'view', 'product')
        can_delete_order = has_permission(request.user, 'delete', 'order')
        can_edit_product = has_permission(request.user, 'edit', 'product')

        return Response({
            "can_view_product": can_view_product,
            "can_delete_order": can_delete_order,
            "can_edit_product": can_edit_product,
        })