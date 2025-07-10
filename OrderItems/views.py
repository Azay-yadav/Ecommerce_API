from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from Orders.serializers import CreateOrderSerializer, OrderSerializer
from Orders.models import Order
from ecomAPP.permissions import IsCustomerUser, IsAdminUser  # adjust if your permissions live elsewhere


# CUSTOMER: Place Order
class PlaceOrderView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        serializer = CreateOrderSerializer(data={}, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=201)
        return Response(serializer.errors, status=400)


# CUSTOMER: List Their Orders
class UserOrderListView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# CUSTOMER: Order Detail
class OrderDetailView(APIView):
    permission_classes = [IsCustomerUser]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# ADMIN: List All Orders
class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# ADMIN: Update Order
class AdminOrderUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
