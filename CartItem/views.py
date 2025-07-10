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
from .models import Product, CartItem
from .serializers import (
    CartItemSerializer
)



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
