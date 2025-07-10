from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect

# Swagger Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce Platform API",
        default_version='v1',
        description=(
            "Comprehensive RESTful API for your e-commerce platform, "
            "supporting customers, admins, and optional sellers."
        ),
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@yourcompany.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Optional: Redirect root '/' to Swagger docs
    path('', lambda request: redirect('/swagger/', permanent=False)),

    # Django Admin
    path('admin/', admin.site.urls),

    # Main app APIs
    path('api/', include('CartItem.urls')),
    path('api/', include('Categories.urls')),
    path('api/', include('OrderItems.urls')),
    path('api/', include('Orders.urls')),
    path('api/', include('products.urls')),
    path('api/', include('Users.urls')),

    # Swagger & ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
