from rest_framework import serializers
from .models import Item,Order
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ItemSerializer(serializers.ModelSerializer):
    user_name = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'user_name',
            'item_name',
            'item_desc',
            'item_price',
            'item_image',
            'is_available',
            'created_at',
            'is_deleted',
            'deleted_at',
        ]

    def validate_item_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Item price must be a positive number.")
        return value

    def validate(self, data):
        if data['item_name'].lower() == data['item_desc'].lower():
            raise serializers.ValidationError("Item name and description cannot be the same.")
        return data

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "items"]    