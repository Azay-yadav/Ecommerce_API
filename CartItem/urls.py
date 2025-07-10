from django.urls import path
from .views import (
    CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView
)

urlpatterns = [

    # -------------------
    # CART MANAGEMENT
    # -------------------
    path('api/cart/', CartView.as_view(), name='view-cart'),
    path('api/cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/cart/update/<int:pk>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('api/cart/remove/<int:pk>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
]
