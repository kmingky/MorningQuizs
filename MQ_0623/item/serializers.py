from rest_framework import serializers

from .models import Category as CategoryModel
from .models import Item as ItemModel
from .models import Order as OrderModel
from .models import ItemOrder as ItemOrderModel


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"


class ItemModelSerializer(serializers.ModelSerializer):
    category = CategoryModelSerializer()

    class Meta:
        model = ItemModel
        fields = ["id", "name", "category", "image_url", "category_id"]


class OrderModelSerializer(serializers.ModelSerializer):
    item = ItemModelSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ["delivery_address", "order_date"]


class ItemOrderModelSerializer(serializers.ModelSerializer):
    order = OrderModelSerializer(read_only=True)
    item = ItemModelSerializer(many=True)
    item_name = serializers.ReadOnlyField(source="item.name")

    class Meta:
        model = ItemOrderModel
        fields = ["id", "order", "item_name", "item_count"]
