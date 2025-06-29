from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    LogoutView,
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    PlaceOrderView,
    UserOrderListView,
    OrderDetailView,
    AdminOrderListView,
    AdminOrderUpdateView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    # Auth
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    # Categories
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Products
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Cart
    path('api/cart/', CartView.as_view(), name='view-cart'),
    path('api/cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/cart/update/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('api/cart/remove/<int:pk>/', RemoveCartItemView.as_view(), name='remove-cart-item'),

    # Orders (User)
    path('api/orders/', UserOrderListView.as_view(), name='user-orders'),
    path('api/orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('api/orders/place/', PlaceOrderView.as_view(), name='place-order'),

    # Orders (Admin)
    path('api/admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('api/admin/orders/<int:pk>/', AdminOrderUpdateView.as_view(), name='admin-order-update'),

    # User Management (Admin)
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
