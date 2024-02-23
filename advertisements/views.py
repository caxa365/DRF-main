from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.permissions import CreateOrReadOnly
from advertisements.serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .models import Advertisement
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Пермишен, который разрешает доступ только авторам объекта для редактирования его.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить чтение запросов любому пользователю.
        # Разрешить запись только авторам объекта.
        return obj.creator == request.user

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []