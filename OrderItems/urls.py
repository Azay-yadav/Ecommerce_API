from django.urls import path
from .views import PlaceOrderView, UserOrderListView, OrderDetailView, AdminOrderListView, AdminOrderUpdateView

urlpatterns = [
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/', UserOrderListView.as_view(), name='user-orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-orders'),
    path('admin/orders/<int:pk>/update/', AdminOrderUpdateView.as_view(), name='admin-order-update'),
]
