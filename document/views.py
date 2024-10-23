from rest_framework import generics, viewsets
from .models import Document
from .serializer import DocumentSerializer
from rest_framework.permissions import IsAuthenticated


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    

class DocumentListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка документов и создания нового документа.
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращаем только документы текущего пользователя"""
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления документа.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        """Возвращаем только документы текущего пользователя"""
        return Document.objects.filter(user=self.request.user)
