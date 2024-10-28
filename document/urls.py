from django.urls import path, include
from .apps import DocumentConfig
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

app_name = DocumentConfig.name

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

schema_view = get_schema_view(
    openapi.Info(
        title="Document API",
        default_version='v1',
        description="API для управления документами",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
