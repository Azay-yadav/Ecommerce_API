from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from ecomAPP.models import Product, Order, OrderItem, CartItem, Category
from django.core.mail import send_mail
import random
from .models import User

User = get_user_model()

# USER SERIALIZERS
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'role': {'default': 'customer'}}

    def create(self, validated_data):
        # Create user instance with inactive status
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'customer'),
            is_active=False  # new user is inactive until OTP is verified
        )
        user.set_password(validated_data['password'])

        # Generate random 6-digit OTP
        otp_code = f"{random.randint(100000, 999999)}"
        user.verification_code = otp_code
        user.save()

        # Send email with OTP
        send_mail(
            subject="Your Account Verification Code",
            message=f"Hi {user.username},\n\nYour OTP for account verification is: {otp_code}\n\nThank you for registering.",
            from_email="ajaykumaryadav02042000@gmail.com",  # Or use settings.DEFAULT_FROM_EMAIL for dynamic config
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")

        if user.verification_code != otp:
            raise serializers.ValidationError("Invalid OTP.")

        return data

    def save(self, **kwargs):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)
        user.is_active = True
        user.verification_code = None  # clear OTP after verification
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user


class LogoutSerializer(serializers.Serializer):
    def validate(self, data):
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active']


# CATEGORY SERIALIZER
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


# PRODUCT SERIALIZER
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'stock', 'image',
            'category', 'category_id', 'created_at', 'updated_at', 'seller'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'seller']


# CART ITEM SERIALIZER
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']

    def create(self, validated_data):
        product = validated_data.pop('product')
        cart_item = CartItem.objects.create(product=product, **validated_data)
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


# ORDER ITEM SERIALIZER
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price_at_order_time']
        read_only_fields = ['id', 'price_at_order_time']


# ORDER SERIALIZER
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount', 'user']


class CreateOrderSerializer(serializers.Serializer):
    def validate(self, data):
        user = self.context['request'].user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = CartItem.objects.filter(user=user)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=user, total_amount=total_amount)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_order_time=item.product.price
            )
            # Optionally decrease stock: item.product.stock -= item.quantity

        cart_items.delete()
        return order
