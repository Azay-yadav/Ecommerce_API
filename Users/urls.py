from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, LogoutView, VerifyOTPView,
    AdminOrderListView, AdminOrderUpdateView,
    UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserOrderListView,CheckPermissionView
)

urlpatterns = [
    path('check-permissions/', CheckPermissionView.as_view(), name='check-permissions'),

    # AUTH & REGISTRATION
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),


    # USER ORDERS
    path('api/orders/', UserOrderListView.as_view(), name='user-orders'),


    # ADMIN ORDERS
    path('api/admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('api/admin/orders/<int:pk>/', AdminOrderUpdateView.as_view(), name='admin-order-update'),


    # USER MANAGEMENT (ADMIN)
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
