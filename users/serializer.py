from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
# from .models import VerificationCode
import random
from config.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )

        # send_mail(
        #     'Ваш код верификации',
        #     f'Ваш код: {code}',
        #     EMAIL_HOST_USER,
        #     [user.email],
        #     fail_silently=False,
        # )

        return user
