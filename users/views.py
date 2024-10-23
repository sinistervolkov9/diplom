from django.core.mail import send_mail
from django.conf import settings
from .serializer import RegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.generate_verification_code()

            send_mail(
                'Подтверждение регистрации',
                f'Ваш код для подтверждения регистрации: {user.verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response(
                {'message': 'Пользователь зарегистрирован, проверьте свою почту для получения кода подтверждения.'},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            user = User.objects.get(verification_code=code)
            user.is_active = True
            # user.verification_code = None
            user.save()
            return Response({'detail': 'Учетная запись успешно активирована!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Неверный код верификации.'}, status=status.HTTP_400_BAD_REQUEST)
