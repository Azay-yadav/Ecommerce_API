from rest_framework import serializers
from django.contrib.auth import get_user_model
from Categories.models import Category
from django.core.mail import send_mail
import random
from Users.models import User

User = get_user_model()


# CATEGORY SERIALIZER
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
