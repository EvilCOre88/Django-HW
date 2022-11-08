from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist

from .filters import AdvertisementFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrAdmin, IsOwnerOrNotDraft

from .models import Advertisement, Favourite
from .serializers import AdvertisementSerializer

from django.db.models import Q


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        if self.action == 'retrieve':
            return [IsOwnerOrNotDraft()]
        return []

    def list(self, request, *args, **kwargs):
        try:
            queryset = Advertisement.objects.all().exclude(~Q(creator=request.user), status='DRAFT')
            queryset = self.filter_queryset(queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
            return Response(serializer.data)
        except TypeError:
            queryset = Advertisement.objects.all().exclude(status='DRAFT')
            queryset = self.filter_queryset(queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_favourite(self, request, pk=None):
        advertisement = self.get_object()
        if request.user == advertisement.creator:
            return Response({'Ошибка': 'Вы не можете добавить свое объявление в избранное'})
        try:
            Favourite.objects.get(advertisement=advertisement, user=request.user)
            return Response({'Ошибка': 'Вы уже добавили это объявление в избранное'})
        except ObjectDoesNotExist:
            Favourite(advertisement=advertisement, user=request.user).save()
            return Response({'Успех!': 'Объявление добавлено в избранное'})
        except TypeError:
            return Response({'Ошибка': 'Только зарегестрированные пользователи могут добавлять объявления в избранное'})

    @action(detail=True, methods=['delete'])
    def delete_from_favourite(self, request, pk=None):
        advertisement = self.get_object()
        try:
            favourite = Favourite.objects.get(advertisement=advertisement, user=request.user)
            favourite.delete()
            return Response({'Успех!': 'Вы удалили объявление из избранного'})
        except ObjectDoesNotExist:
            return Response({'Ошибка': 'У вас в избранном нет этого объявления'})
        except TypeError:
            return Response({'Ошибка': 'Только зарегестрированные пользователи могут удалять объявления из избранного'})

    @action(detail=False, methods=['get'])
    def favourite(self, request):
        try:
            advertisements = Advertisement.objects.filter(favourites__user=request.user)
            serializer = AdvertisementSerializer(advertisements, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response({'Ошибка': 'Только зарегестрированные пользователи могут смотреть избранные объявления'})
