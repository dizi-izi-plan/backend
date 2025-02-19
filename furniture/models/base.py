from django.contrib.gis.db import models as gis_models
from django.db import models


class Coordinate(models.Model):
    """Модель координаты."""

    x = models.PositiveIntegerField(
        verbose_name='X',
    )
    y = models.PositiveIntegerField(
        verbose_name='Y',
    )

    def __str__(self):
        return f'x={self.x}, y={self.y}'


class PlacementCoordinates(gis_models.Model):
    """Abstract model with a pointer to a room and coordinates."""

    room = models.ForeignKey(
        "RoomLayout",
        on_delete=models.CASCADE,
        verbose_name='Комната',
        related_name='%(class)ss',
    )
    shape = gis_models.PolygonField(
        verbose_name='Координаты объекта',
        srid=0,
        null=True
    )

    class Meta:
        abstract = True
