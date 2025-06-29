from django.contrib import admin
from django.urls import path, include, re_path
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

    # Your main app API
    path('api/', include('ecomAPP.urls')),

    # Swagger & ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
