from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        creating_user = self.context["request"].user.id
        if not creating_user:
            raise ValidationError('Ошибка: только зарегестрированные пользователи могут создавать объявления')
        if self.context['request'].method == 'PATCH' and data.get('status') in ['CLOSED', 'DRAFT']:
            return data
        user_open_ads = Advertisement.objects.filter(creator=creating_user, status='OPEN')
        if len(user_open_ads) >= 10:
            raise ValidationError('Вам доступно максимум 10 открытых объявлений')
        return data
