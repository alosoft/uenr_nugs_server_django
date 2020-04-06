from django.contrib.auth.models import User, Group
from rest_framework import serializers

from shop.models import Order, OrderItem, Product, Color, Size, Review
from djoser.serializers import UserSerializer


# from news.serializers import ImageSerializer


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user_details', 'owner', 'title', 'message', 'product', 'date', 'stars')


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'color_code')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name', 'size_value')


class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)

    # images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'created', 'updated', 'description', 'diameter', 'discount', 'weight', 'width', 'featured',
            'unlimited', 'height', 'length', 'price', 'quantity', 'status', 'category', 'images', 'features',
            'specifications', 'sizes', 'colors', 'color_list', 'size_list')


class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'size', 'quantity',
                  'color', 'owner', 'created', 'date', 'color_name', 'size_name')


class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ('id', 'items', 'owner', 'status', 'created', 'date', 'price', 'description', 'transaction', 'reason')
