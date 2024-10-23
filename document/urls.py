from django.urls import path, include
from .apps import DocumentConfig
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet

app_name = DocumentConfig.name

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
]
