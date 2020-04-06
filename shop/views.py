from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
import re
from shop.models import Order, OrderItem, Product, Review
from shop.serializers import OrderItemSerializer, ReviewSerializer, OrderSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.all().order_by('-date_joined')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        featured = self.request.GET.get('featured')
        cat = self.request.GET.get('category')
        if featured:
            queryset = queryset.filter(featured=True)
        if cat:
            queryset = queryset.filter(category=cat)
        # serializer = ProductSerializer(queryset, many=True)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = ProductSerializer(user)
        return Response(serializer.data)


@api_view(['GET'])
def set_transaction_id(request):
    transaction_id = request.GET.get('transaction_id')
    order_id = request.GET.get('order_id')
    try:
        order = Order.objects.get(pk=int(order_id))
        order.transaction = int(transaction_id)
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_206_PARTIAL_CONTENT)
    except Order.DoesNotExist:
        return Response({'message': f'no order with this transaction id:{transaction_id}'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def confirm(request):
    # // code=000&status=successful&reason=transaction20%successful&transaction_id=000000000000
    transaction_id = request.GET.get('transaction_id')
    server_status = request.GET.get('status')
    reason = request.GET.get('reason')
    code = request.GET.get('code')
    if not code:
        return Response({'message': 'failed'}, status=status.HTTP_403_FORBIDDEN)
    if code == '000' and len(transaction_id) == 12:
        try:
            order = Order.objects.get(transaction=int(transaction_id))
            order.transaction = int(transaction_id)
            order.status = 'Paid'
            order.save()
            return Response({'message': 'order marked as paid'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': f'no order with this transaction id:{transaction_id}'}, status=status.HTTP_404_NOT_FOUND)
    if len(transaction_id) < 12:
        return Response({'message': f'transaction id should be 12:{transaction_id}'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': reason}, status=status.HTTP_403_FORBIDDEN)
    # return Response({'status': server_status, 'reason': reason}, sstatus=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def order(request):
    item_ids = request.GET.get('ids')
    user_id = request.GET.get('user_id')
    ids_list = re.findall('\d+', item_ids)
    new_order = Order.objects.create(owner_id=user_id)
    for id in ids_list:
        new_order.items.add(int(id))
    new_order.save()
    return Response(OrderSerializer(new_order).data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user orders to be viewed or edited
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_class = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.all().filter(owner=self.request.user.id)
        print(self.request.user.id)
        print(queryset.__len__())
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = OrderSerializer(user)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user order items to be viewed or edited
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_class = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id']

    def list(self, request, *args, **kwargs):
        parent_order_id = request.GET.get('order_id')
        queryset = OrderItem.objects.all()
        if parent_order_id:
            print(parent_order_id)
            queryset = Order.objects.get(pk=int(parent_order_id)).items.all()
        serializer = OrderItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = OrderItem.objects.all()
        user = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = OrderItemSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users product reviews to be viewed or edited.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        queryset = Review.objects.all()
        if product_id:
            queryset= queryset.filter(product=int(product_id))
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Review.objects.all()
        review = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'partial update reached'})