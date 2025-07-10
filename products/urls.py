from django.urls import path
from .views import (
    ProductListCreateView, ProductDetailView
)

urlpatterns = [

    # -------------------
    # PRODUCT MANAGEMENT
    # -------------------
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
]
