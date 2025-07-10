from rest_framework import generics, filters, permissions
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from ecomAPP.permissions import IsAdminUser, IsSellerUser, IsCustomerUser
from .models import Product
from .serilaizers import ProductSerializer


# UPDATED PRODUCT VIEWS (pagination, filtering, search, ordering)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['category__name']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role not in ['admin', 'seller']:
            raise permissions.PermissionDenied("Only admin/seller can create products.")
        serializer.save(seller=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role not in ['admin', 'seller']:
            raise permissions.PermissionDenied("Only admin/seller can update products.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_authenticated or self.request.user.role not in ['admin', 'seller']:
            raise permissions.PermissionDenied("Only admin/seller can delete products.")
        instance.delete()
