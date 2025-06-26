from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    RegisterView,
    ProductListView,
    ProductDetailView,
    CartView,
    AddToCartView,
    PlaceOrderView,
    UserOrderListView,
)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),

    # Cart
    path('cart/', CartView.as_view(), name='view-cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),

    # Orders
    path('orders/', UserOrderListView.as_view(), name='user-orders'),
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
]
