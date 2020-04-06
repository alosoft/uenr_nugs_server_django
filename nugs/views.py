from django.shortcuts import render
from nugs.models import Bloc
from nugs.serializers import BlocSerializer
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
class BlocViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bloc to be viewed or edited
    """

    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    permission_class = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = Bloc.objects.all()
        serializer = BlocSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Bloc.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = BlocSerializer(user)
        return Response(serializer.data)