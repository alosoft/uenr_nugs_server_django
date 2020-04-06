from djoser.serializers import UserCreateSerializer

from shop.serializers import ProductSerializer
from users.models import User


class UserSerializer(UserCreateSerializer):
    cart = ProductSerializer(many=True, read_only=True)
    favorite = ProductSerializer(many=True, read_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'number', 'password', 'image', 'username', 'bookmarks',
                  'favorite', 'cart']
