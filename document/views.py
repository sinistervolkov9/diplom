from rest_framework import generics
from .models import Document
from .serializer import DocumentSerializer
from rest_framework.permissions import IsAuthenticated


class DocumentListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка документов и создания нового документа.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления документа.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
