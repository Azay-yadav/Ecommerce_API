from django.urls import path
from .views import (
    PlaceOrderView, UserOrderListView, OrderDetailView,
)

urlpatterns = [

    # -------------------
    # USER ORDERS
    # -------------------
    path('api/orders/', UserOrderListView.as_view(), name='user-orders'),
    path('api/orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('api/orders/place/', PlaceOrderView.as_view(), name='place-order'),

]
