from .models import Document
from .serializer import DocumentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from .tasks import send_user_notification
from rest_framework.exceptions import NotAuthenticated
from users.permissions import IsAdminOrReadOnly


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра списка документов и получения информации о документе.
    Создание нового документа также остается в этом ViewSet.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """Возвращаем документы в зависимости от статуса и роли пользователя."""
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated("Пользователь не аутентифицирован.")
        if user.is_staff:
            return Document.objects.all()
        return Document.objects.filter(user=user) | Document.objects.filter(status='approved')

    def perform_create(self, serializer):
        """Создаем новый документ и привязываем его к текущему пользователю."""
        serializer.save(user=self.request.user)


class DocumentUpdateView(generics.UpdateAPIView):
    """
    Представление для изменения документа (PUT и PATCH запросы).
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_update(self, serializer):
        """После обновления отправляем уведомление пользователю."""
        instance = serializer.save()
        if 'status' in serializer.validated_data:
            send_user_notification.delay(
                user_email=instance.user.email,
                document_status=instance.get_status_display(),
                document_title=instance.title
            )


class DocumentDeleteView(generics.DestroyAPIView):
    """
    Представление для удаления документа.
    """
    queryset = Document.objects.all()
    permission_classes = [IsAdminOrReadOnly]
