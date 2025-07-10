from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from Orders.models import Order
from CartItem.models import CartItem
from OrderItems.models import OrderItem
from Categories.models import Category
from django.core.mail import send_mail
import random
from .models import User
from OrderItems.serializers import OrderItemSerializer

User = get_user_model()


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

        cart_items.delete()
        return order
