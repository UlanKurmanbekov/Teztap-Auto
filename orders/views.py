from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if user.is_anonymous:
            return Response('Пользователь должен быть авторизован', status=status.HTTP_401_UNAUTHORIZED)

        orders = self.queryset.filter(user=user)
        return orders

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

