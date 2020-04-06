# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from news.models import News
from shop.models import Product
from users.models import User
from users.serializers import UserSerializer
from shop.serializers import ProductSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'partial update reached'})

@api_view(['GET'])
# @renderer_classes((JSONRenderer))
def cart(request):
    """
    API endpoint that allows users product in cart to be viewed.
    """
    user_id = request.GET.get('user_id')
    print('-----------------------------came through-----------------------')
    try:
        user = User.objects.get(pk=int(user_id))
        query_set = user.cart.all()
        serializer = ProductSerializer(query_set, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'no user with that id'})

@api_view(['GET'])
# @renderer_classes((JSONRenderer))
def favorite(request):
    """
    API endpoint that allows users favorite product to be viewed.
    """
    user_id = request.GET.get('user_id')
    print('-----------------------------came through-----------------------')
    try:
        user = User.objects.get(pk=int(user_id))
        query_set = user.favorite.all()
        serializer = ProductSerializer(query_set, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'no user with that id'})



def update(request):
    news_id = request.GET.get('news_id')
    user_id = request.GET.get('user_id')
    product_id = request.GET.get('product_id')
    cart = request.GET.get('cart')
    if user_id:
        try:
            user = User.objects.get(pk=int(user_id))
            if user:
                if news_id:
                    try:
                        user.bookmarks.get(pk=int(news_id))
                        user.bookmarks.remove(int(news_id))
                        return HttpResponse('removed')
                    except News.DoesNotExist:
                        user.bookmarks.add(int(news_id))
                        return HttpResponse('added')
                elif product_id:
                    try:
                        user.cart.get(pk=int(product_id))
                        user.cart.remove(int(product_id))
                        return HttpResponse('removed')
                    except Product.DoesNotExist:
                        user.cart.add(int(product_id))
                        return HttpResponse('added')
                elif cart:
                    try:
                        user.favorite.get(pk=int(cart))
                        user.favorite.remove(int(cart))
                        return HttpResponse('removed')
                    except Product.DoesNotExist:
                        user.favorite.add(int(cart))
                        return HttpResponse('added')
        except User.DoesNotExist:
            return HttpResponse('no user found')

    return HttpResponse('no action taken')
