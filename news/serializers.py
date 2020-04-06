from django.contrib.auth.models import User, Group
from rest_framework import serializers

from news.models import Comments, Media, News
from users.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['image']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'media_type', 'image', 'created', 'updated', 'video']


class CommentsSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'created', 'body', 'owner', 'news_id', 'date')


class NewsSerializer(serializers.ModelSerializer):
    image = MediaSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'category', 'created',
                  'updated', 'body', 'images', 'image', 'comments', 'comments_count', 'date')
