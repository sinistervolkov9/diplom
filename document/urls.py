from django.urls import path
from .apps import DocumentConfig
from rest_framework.routers import DefaultRouter
from .views import DocumentListCreateView, DocumentDetailView

app_name = DocumentConfig.name

# router = DefaultRouter()
# router.register(r'habits', DocumentViewSet)

urlpatterns = [
    path('documents/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
]
