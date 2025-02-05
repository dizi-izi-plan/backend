from rest_framework import serializers

from furniture.models import Furniture, RoomType


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ("name", "slug")


class FurnitureSerializer(serializers.ModelSerializer):
    """Сериализатор для мебели."""

    type_of_rooms = RoomTypeSerializer()

    class Meta:
        fields = (
            "id",
            "name",
            "name_english",
            "length",
            "width",
            "length_access",
            "width_access",
            "type_of_rooms",
            "image"
        )
        model = Furniture
