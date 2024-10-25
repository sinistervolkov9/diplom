from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """
        Создаем неактивного пользователя до верификации
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        return user


class VerifyCodeSerializer(serializers.Serializer):
    """
    Сериализатор для верификации кода пользователя
    """
    code = serializers.IntegerField(help_text='Код, отправленный на почту для подтверждения')
