from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from news.models import Comments, Media, News
from news.serializers import CommentsSerializer, MediaSerializer, NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows news to be viewed or edited.
    """
    queryset = News.objects.all().order_by('-created')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']

    def retrieve(self, request, *args, **kwargs):
        queryset = News.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = NewsSerializer(user)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        queryset_list = News.objects.all()
        query = self.request.GET.get('query')
        category = self.request.GET.get('category')
        comments = self.request.GET.get('comments')
        ordering = self.request.GET.get('manual_ordering')
        limit = self.request.GET.get('limit')

        for new in queryset_list:
            count = Comments.objects.all().filter(news_id=new.pk).__len__()
            new.comments_count = count
            # new.save()

        if comments:
            queryset_list = queryset_list.annotate(
                num_comments=Count('comments')).order_by('-num_comments')[:10]

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(body__contains=query)
            )

        if category:
            queryset_list = queryset_list.filter(
                Q(category__iexact=category)
            )
            if ordering:
                queryset_list = queryset_list.annotate(
                    num_comments=Count('comments')).order_by('-num_comments' if '-' in ordering else 'num_comments')

        if limit:
            queryset_list = queryset_list[:int(limit)]

        return queryset_list


class MediaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows media to be viewed or edited.
    """

    queryset = Media.objects.all().order_by('-created')
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = Media.objects.all()
        serializer = MediaSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Media.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = MediaSerializer(user)
        return Response(serializer.data)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comment to be viewed or edited.
    """

    queryset = Comments.objects.all().order_by('-created')
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comments.objects.all()
        news_id = self.request.GET.get('news_id')

        if news_id:
            queryset_list = queryset_list.filter(
                Q(news_id__iexact=news_id)
            )

        return queryset_list

    def retrieve(self, request, *args, **kwargs):
        queryset = Comments.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = CommentsSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        news_id = self.request.GET.get('news_id')
        news = News.objects.all().get(pk=int(news_id))
        comment = serializer.save(owner=self.request.user, news_id=news_id)
        news.comments.add(comment)
        return super().perform_create(serializer)
