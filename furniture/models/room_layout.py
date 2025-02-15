from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from furniture.utils import get_name
from furniture.validators import minimum_len_width_validator

User = get_user_model()


class Room(models.Model):
    """Model of room."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Пользователь',
    )
    name = models.CharField(
        'Название комнаты',
        max_length=settings.MAX_LENGTH_ROOM_NAME,
    )
    first_wall = models.PositiveIntegerField(
        'Длина 1 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )
    second_wall = models.PositiveIntegerField(
        'Длина 2 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )
    third_wall = models.PositiveIntegerField(
        'Длина 3 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )
    fourth_wall = models.PositiveIntegerField(
        'Длина 4 стены',
        help_text='Длина стены в мм',
        validators=(minimum_len_width_validator,),
    )

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self) -> str:
        return f"Комната: {self.name}"


class RoomLayout(models.Model):
    """Model of room layout."""

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='layouts',
        verbose_name='Комната',
    )
    name = models.CharField(
        'Название планировки',
        max_length=settings.MAX_LENGTH_ROOM_NAME,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
        db_index=True,
    )
    furniture_placement = models.ManyToManyField(
        'Furniture',
        through='FurniturePlacement',
    )

    class Meta:
        verbose_name = 'Планировка'
        verbose_name_plural = 'Планировки'

    def __str__(self) -> str:
        return f"Проект {self.name} пользователя {self.user.email}"

    def copy(self, request):
        """Возвращает копию объекта комнаты.

        С новым первичным ключом, но теми же значениями атрибутов.

        M2M отношения не копируются.
        """
        return RoomLayout.objects.create(
            user=self.user,
            name=get_name(self.user),
            first_wall=self.first_wall,
            second_wall=self.second_wall,
            third_wall=self.third_wall,
            fourth_wall=self.fourth_wall,
        )
