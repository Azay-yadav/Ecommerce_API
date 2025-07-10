from rest_framework import serializers
from django.contrib.auth import get_user_model
import random
from .models import CartItem
from products.models import Product
from products.serilaizers import ProductSerializer

User = get_user_model()



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

