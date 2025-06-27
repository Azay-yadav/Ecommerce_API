from django.urls import path
from .views import ProductCreateView
from .views import CategoryCreateView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    LogoutView,
    RegisterView,
    ProductCreateView,
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
    path('logout/', LogoutView.as_view(), name='logout'),

    # Categories
    path('categories/', CategoryCreateView.as_view(), name='category-list-create'),
    
    # Products
     path('products/', ProductCreateView.as_view(), name='product-list-create'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),

    # Cart
    path('cart/', CartView.as_view(), name='view-cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),

    # Orders
    path('orders/', UserOrderListView.as_view(), name='user-orders'),
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
]
