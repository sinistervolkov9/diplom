from .models import Document
from .serializer import DocumentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, permissions
from .tasks import send_user_notification


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращаем документы в зависимости от статуса и роли пользователя."""
        user = self.request.user
        if user.is_staff:
            return Document.objects.all()
        return Document.objects.filter(status='approved', user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DocumentListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка документов и создания нового документа.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращаем только одобренные админом документы"""
        user = self.request.user
        if user.is_staff:
            return Document.objects.all()
        return Document.objects.filter(status='approved')

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


class DocumentUpdateView(generics.UpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if 'status' in serializer.validated_data:
            send_user_notification.delay(
                user_email=instance.user.email,
                document_status=instance.get_status_display(),
                document_title=instance.title
            )


class DocumentDeleteView(generics.DestroyAPIView):
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated]
