from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from furniture.models import (
    DoorPlacement,
    Furniture,
    FurniturePlacement,
    PowerSocketPlacement,
    RoomLayout,
    WindowPlacement,
)
from furniture.filters import FurnitureFilter
from furniture.serializers import (
    FurnitureSerializer,
    RoomLayoutSerializer,
)
from api.permissions import IsTariffAccepted
from furniture.utils import send_pdf_file


class FurnitureViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных о мебели."""

    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FurnitureFilter


class RoomViewSet(viewsets.ModelViewSet):
    """Получение и изменение планировки."""

    serializer_class = RoomLayoutSerializer

    permission_classes = (IsAuthenticated, IsTariffAccepted)

    def get_queryset(self):
        """Получение данных о помещении только пользователя запроса."""
        if self.request.user.is_authenticated:
            return self.request.user.rooms.all()
        return RoomLayout.objects.none()

    def perform_create(self, serializer):
        """Назначение данных для обработки запроса."""
        user = self.request.user
        serializer.save(user=user)

    def list(self, request, *args, **kwargs):
        """Список комнат.

        Получение списка комнат. Доступно всем пользователям.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Создание комнаты.

        Создание новой комнаты. Доступно авторизованным пользователям.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Получение комнаты.

        Получение информации о комнате по идентификатору.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Обновление комнаты.

        Обновление информации о комнате. Доступно владельцу комнаты.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление комнаты."""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление комнаты.

        Удаление существующей комнаты. Доступно владельцу комнаты.
        """
        return super().destroy(request, *args, **kwargs)


class RoomCopyView(APIView):
    """Создаем копию объекта `Room`.

    Выполняется по произвольному пост запросу на url /api/v1/rooms/pk/.
    """

    @staticmethod
    def _copy_object(
        model: [DoorPlacement | WindowPlacement | PowerSocketPlacement],
        orig_room: RoomLayout,
        new_room: RoomLayout,
    ):
        models = model.objects.filter(room=orig_room)
        for model in models:
            model.pk = None
            model.room = new_room
            model.save()

    def get(self, request, pk):
        """Получаем планировку с заданным `pk`."""
        orig_room = get_object_or_404(RoomLayout, pk=pk)
        serializer = RoomLayoutSerializer(orig_room)
        return Response(serializer.data)

    def post(self, request, pk):
        """Создаем копию планировки с заданным `pk`."""
        orig_room = get_object_or_404(RoomLayout, pk=pk)
        new_room = orig_room.copy(request)
        new_room.save()
        serializer = RoomLayoutSerializer(new_room)
        furniture = Furniture.objects.filter(room=orig_room)

        for furn in furniture:
            placement = FurniturePlacement.objects.get(
                furniture=furn,
                room=orig_room,
            )
            FurniturePlacement.objects.create(
                room=new_room,
                furniture=furn,
                nw_coordinate=placement.nw_coordinate,
                ne_coordinate=placement.ne_coordinate,
                sw_coordinate=placement.sw_coordinate,
                se_coordinate=placement.se_coordinate,
            )
        [
            self._copy_object(obj, orig_room, new_room)
            for obj in [
                DoorPlacement,
                WindowPlacement,
                PowerSocketPlacement,
            ]
        ]

        return Response(serializer.data)

    def patch(self, request, pk):
        """Изменяем планировку с заданным `pk`."""
        instance = get_object_or_404(RoomLayout, pk=pk)
        instance.name = request.data.get("name")
        instance.save()
        serializer = RoomLayoutSerializer(instance)
        return Response(serializer.data)


class SendPDFView(APIView):
    """Отправка pdf файла на почту."""
    parser_classes = (MultiPartParser,)
    permission_classes = (
        IsAuthenticated,
        IsTariffAccepted,
    )

    def post(self, request, format="pdf"):
        """Загружаем планировку в формате PDF."""
        up_file = request.FILES["file"]
        subj = "План размещения мебели"
        text = "В приложении подготовленный план размещения мебели"
        email = request.user.email
        return send_pdf_file(subj, email, up_file, text)


