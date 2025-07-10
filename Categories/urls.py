from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
)

urlpatterns = [

    # -------------------
    # CATEGORY MANAGEMENT
    # -------------------
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
