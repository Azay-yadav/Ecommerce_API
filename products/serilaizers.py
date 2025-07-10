from rest_framework import serializers
from django.core.mail import send_mail
import random
from .models import Product
from Categories.models import Category
from Categories.serializers import CategorySerializer
from django.contrib.auth import get_user_model
User = get_user_model()




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
