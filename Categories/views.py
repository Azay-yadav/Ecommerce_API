from rest_framework import generics, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
import requests
from .PayPal import get_paypal_access_token
from .permissions import IsAdminUser, IsSellerUser, IsCustomerUser
from .models import Category
from Orders.models import Order
from Orders import views
from .serializers import (
    CategorySerializer
)


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

