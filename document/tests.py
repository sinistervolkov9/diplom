from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from document.models import Document


class DocumentPermissionsTest(APITestCase):

    def setUp(self):
        """
        Создание тестовых данных
        """
        # Обычный пользователь
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='User',
            email='user@user.ru',
            password='userpassword'
        )

        # Админ
        self.admin_user = self.User.objects.create_superuser(
            username='Admin',
            email='admin@admin.ru',
            password='adminpassword'
        )

        # Документы
        # Документ обычного пользователя в ожидании
        self.user_document = Document.objects.create(
            user=self.user,
            file='documents/user_doc.docx',
            title='Документ Юзера',
            status='pending'
        )

        # Документ админа отклоненный
        self.admin_document = Document.objects.create(
            user=self.admin_user,
            file='documents/admin_doc.docx',
            title='Документ Админа',
            status='rejected'
        )

         # Документы обычного пользователя одобренный
        self.approved_document = Document.objects.create(
            user=self.user,
            file='documents/approved_doc.docx',
            title='Одобренный Документ',
            status='approved'
        )

        # URL для детального представления документа
        self.document_detail_url = reverse(
            'document:document-detail',
            kwargs={'pk': self.user_document.id}
        )

    def test_user_cannot_change_or_delete_document(self):
        """
        Обычные пользователи не могут изменять или удалять документы
        """
        self.client.force_authenticate(user=self.user)

        # Попытка изменения документа
        response = self.client.patch(self.document_detail_url, {'title': 'New Title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Попытка удаления документа
        response = self.client.delete(self.document_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_change_or_delete_document(self):
        """
        Админы могут изменять и удалять документы.
        """
        self.client.force_authenticate(user=self.admin_user)

        # Попытка изменения документа
        response = self.client.patch(self.document_detail_url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Перезагружаем документ и проверяем, что заголовок изменился
        self.user_document.refresh_from_db()  # Перезагрузка объекта
        self.assertEqual(self.user_document.title, 'Документ обновленный')

        # Попытка удаления документа
        response = self.client.delete(self.document_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_only_see_own_and_approved_documents(self):
        """
        Обычные пользователи могут видеть только свои документы и одобренные.
        """
        self.client.force_authenticate(user=self.user)

        # Получаем список документов
        response = self.client.get(reverse('document:document-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка видимых документов
        documents = response.json()
        document_ids = [doc['id'] for doc in documents]

        # Пользователь видит только свои одобренные документы
        self.assertIn(self.approved_document.id, document_ids)  # Видит свой одобренный документ
        self.assertNotIn(self.admin_document.id, document_ids)  # Не видит документ с другим статусом
        self.assertNotIn(self.user_document.id, document_ids)  # Не видит документ с другим статусом

    def test_admin_can_see_all_documents(self):
        """
        Админы могут видеть все документы, включая pending и rejected
        """
        self.client.force_authenticate(user=self.admin_user)

        # Получаем список документов
        response = self.client.get(reverse('document:document-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка видимых документов
        documents = response.json()
        document_ids = [doc['id'] for doc in documents]

        # Админ видит все документы
        self.assertIn(self.user_document.id, document_ids)
        self.assertIn(self.admin_document.id, document_ids)
        self.assertIn(self.approved_document.id, document_ids)

    def test_unauthorized_user_cannot_see_documents(self):
        """
        Неавторизованные пользователи не могут видеть список документов
        """
        # Получить список документов без авторизации
        response = self.client.get(reverse('document:document-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_cannot_see_document_detail(self):
        """
        Неавторизованный пользователь не может видеть отдельный документ
        """
        # Получить документ по id без авторизации
        response = self.client.get(reverse('document:document-detail', kwargs={'pk': self.approved_document.id}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_see_detailed_document_with_any_status(self):
        """
        Админ может видеть детальную информацию любого документа
        """
        self.client.force_authenticate(user=self.admin_user)

        # Проверка доступа к каждому документу
        for document in [self.user_document, self.admin_document, self.approved_document]:
            response = self.client.get(reverse('document:document-detail', kwargs={'pk': document.id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
