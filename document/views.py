from .models import Document
from .serializer import DocumentSerializer
from rest_framework import viewsets
from .tasks import send_user_notification
from rest_framework.exceptions import NotAuthenticated
from users.permissions import IsAdminOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с документами:
    - Просмотр списка документов
    - Получение информации о конкретном документе
    - Создание нового документа
    - Обновление и удаление документа (только для администратора)
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Возвращаем документы в зависимости от статуса и роли пользователя.
        Только администраторы видят все документы.
        """
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated("Пользователь не аутентифицирован.")
        if user.is_superuser:
            return Document.objects.all()
        return Document.objects.filter(user=user, status='approved')

    @swagger_auto_schema(
        operation_description="Создание нового документа",
        responses={201: DocumentSerializer()},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['file', 'title'],
            properties={
                'file': openapi.Schema(type=openapi.TYPE_FILE, description="Файл"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="Название документа"),
            },
        )
    )
    def perform_create(self, serializer):
        """
        Создаем новый документ и привязываем его к текущему пользователю.
        """
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Обновление документа",
        responses={200: DocumentSerializer()},
        request_body=DocumentSerializer
    )
    def perform_update(self, serializer):
        """
        Представление для изменения документа (PUT и PATCH запросы).
        Обновляет документ и отправляет уведомление пользователю, если статус изменён.
        """
        instance = serializer.save()

        if 'status' in serializer.validated_data:
            send_user_notification.delay(
                user_email=instance.user.email,
                document_status=instance.get_status_display(),
                document_title=instance.title
            )

    @swagger_auto_schema(
        operation_description="Удаление документа",
        responses={204: "Документ успешно удалён"}
    )
    def perform_destroy(self, instance):
        """
        Представление для удаления документа.
        """
        instance.delete()

    def get_serializer_context(self):
        return {'request': self.request}
