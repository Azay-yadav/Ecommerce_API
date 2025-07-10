from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import random
from .models import OrderItem
from products.serilaizers import ProductSerializer

User = get_user_model()


# ORDER ITEM SERIALIZER
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price_at_order_time']
        read_only_fields = ['id', 'price_at_order_time']

