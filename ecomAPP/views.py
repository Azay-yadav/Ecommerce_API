from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .permissions import IsAdminUser, IsSellerUser, IsCustomerUser
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from .models import Product, Category, CartItem, Order, User
from .serializers import VerifyOTPSerializer
from .serializers import (
    ProductSerializer, CategorySerializer, CartItemSerializer,
    OrderSerializer, CreateOrderSerializer,
    RegisterSerializer, LogoutSerializer,
    UserSerializer, UpdateUserSerializer,
)


# USER REGISTRATION
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: "User registered successfully"})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                subject = 'mero name kurkur hoo',
                message= 'help me by giving biscuit',
                recipient_list= [user.email],
                fail_silently= False
            )
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


# CATEGORY VIEWS (Admin only)
class CategoryListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=204)


# PRODUCT VIEWS (GET for all, CREATE/UPDATE/DELETE for Seller/Admin)
class ProductListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        if not request.user.is_authenticated or request.user.role not in ['admin', 'seller']:
            return Response({"detail": "Permission denied. Only admin/seller can create products."}, status=403)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.is_authenticated or request.user.role not in ['admin', 'seller']:
            return Response({"detail": "Permission denied. Only admin/seller can update products."}, status=403)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(seller=product.seller)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.is_authenticated or request.user.role not in ['admin', 'seller']:
            return Response({"detail": "Permission denied. Only admin/seller can delete products."}, status=403)
        product.delete()
        return Response(status=204)


# CART VIEWS (Customer only)
class CartView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsCustomerUser]

    @swagger_auto_schema(request_body=CartItemSerializer)
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UpdateCartItemView(APIView):
    permission_classes = [IsCustomerUser]

    def patch(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class RemoveCartItemView(APIView):
    permission_classes = [IsCustomerUser]

    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
        cart_item.delete()
        return Response(status=204)


# ORDER VIEWS (Customer can place & view their own orders)
class PlaceOrderView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        serializer = CreateOrderSerializer(data={}, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=201)
        return Response(serializer.errors, status=400)


class UserOrderListView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# ADMIN ORDER MANAGEMENT
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


class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer


class UserDeleteView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
