from django.urls import path, include
from .apps import DocumentConfig
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentUpdateView, DocumentDeleteView

app_name = DocumentConfig.name

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
    path('documents/<int:pk>/change/', DocumentUpdateView.as_view(), name='document-change'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document-delete'),
]
