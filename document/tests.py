from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from document.models import Document


class DocumentPermissionsTest(APITestCase):

    def setUp(self):
        """Создание тестовых данных"""
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

        # Документ
        self.document = Document.objects.create(
            user=self.user,
            file='documents/sample_doc_psOXPhD.docx',
            title='Документ Юзера',
            status='rejected'
        )

        # URL для изменения и удаления документа
        self.document_change_url = reverse('document:document-change', kwargs={'pk': self.document.id})
        self.document_delete_url = reverse('document:document-delete', kwargs={'pk': self.document.id})

    def test_user_cannot_change_or_delete_document(self):
        """Обычные пользователи не могут изменять или удалять документы"""
        self.client.force_authenticate(user=self.user)

        # Попытка изменения документа
        response = self.client.patch(self.document_change_url, {'title': 'New Title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Попытка удаления документа
        response = self.client.delete(self.document_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_change_or_delete_document(self):
        """Админы могут изменять и удалять документы"""
        self.client.force_authenticate(user=self.admin_user)

        # Попытка изменения документа
        response = self.client.patch(self.document_change_url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверим, что заголовок изменился
        self.document.refresh_from_db()
        self.assertEqual(self.document.title, 'Updated Title')

        # Попытка удаления документа
        response = self.client.delete(self.document_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_only_see_own_and_approved_documents(self):
        """Обычные пользователи можгут видеть только свои документы и одобренные"""
        self.client.force_authenticate(user=self.user)

        # Попытка получить список документов
        response = self.client.get(reverse('document:document-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка видимых документов
        documents = response.json()
        self.assertTrue(any(doc['id'] == self.document.id for doc in documents))  # Видит свои документы
        self.assertFalse(any(doc['status'] == 'rejected' for doc in documents if
                             doc['id'] != self.document.id))  # Не видит отклонённые чужие

    def test_admin_can_see_all_documents(self):
        """Админы могут видеть все документы"""
        self.client.force_authenticate(user=self.admin_user)

        # Получаем список документов
        response = self.client.get(reverse('document:document-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Админ видит все документы
        documents = response.json()
        self.assertTrue(any(doc['id'] == self.document.id for doc in documents))

    def test_unauthorized_user_cannot_see_documents(self):
        """Неавторизованные пользователи не могут видеть список документов"""
        # Попробуем получить список документов без авторизации
        response = self.client.get(reverse('document:document-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_cannot_see_document_detail(self):
        """Неавторизованный пользователь не может видеть отдельный документ"""
        # Документ
        document = Document.objects.create(
            title="Test Document",
            file="test.pdf",
            status="approved",
            user=self.user
        )

        response = self.client.get(reverse('document:document-detail', kwargs={'pk': document.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
