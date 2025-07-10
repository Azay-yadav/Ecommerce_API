from rest_framework import generics, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
import requests
from ecomAPP.permissions import IsCustomerUser
from .models import Order
from .serializers import (
    OrderSerializer, CreateOrderSerializer
)



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


