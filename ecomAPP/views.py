from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from .models import Product, Category, CartItem, Order, OrderItem
from django.contrib.auth import authenticate, login
from .serializers import (
    ProductSerializer, CategorySerializer,
    CartItemSerializer, OrderSerializer,
    RegisterSerializer
)


# USER REGISTRATION

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "User registered successfully", 400: "Bad Request"}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# USER LOGIN
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={200: "Login successful", 400: "Invalid credentials"}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"msg": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# PRODUCT VIEWS

class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]
def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]
def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)


# CART VIEWS (for customers)

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CartItemSerializer,
        responses={201: "Item added to cart", 400: "Invalid data"}
    )
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Link to logged-in user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ORDER VIEWS (for customers)

class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
@swagger_auto_schema(
        request_body=OrderSerializer,
        responses={201: "Ordered placed successfuly", 400: "Bad Request"}
    )
def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Your cart is empty"}, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_amount=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_order_time=item.product.price
            )

        cart_items.delete()  
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)

class UserOrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
