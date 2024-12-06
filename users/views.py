from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from django.utils.encoding import force_bytes, force_str
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from drf_spectacular.utils import extend_schema

from users.models import User
from users.tasks import send_email_task
from users.serializers import UserSerializer, SignUpSerializer, PasswordResetRequestSerializer, \
    PasswordResetConfirmSerializer


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


token_generator = PasswordResetTokenGenerator()


class PasswordResetRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            '200': {'message': 'Ссылка для обновления пароля отправлена на вашу почту.'},
            '404': {'error': 'Пользователь не найден'}
        }
    )
    def post(self, request):
        email = request.user.email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь с такой электронной почтой не найден.'}, status=status.HTTP_404_NOT_FOUND)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_link = request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
        )

        send_email_task.delay(email, reset_link)

        return Response({'message': reset_link}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={'200': {'message': 'Пароль успешно обновлен.'}, '400': {'error': 'Неверный токен или ID'}}
    )
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Неверный токен или ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_generator.check_token(user, token):
            return Response({'error': 'Неверный токен или время токена истекло.'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error': 'Новый пароль обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Пароль был успешно обновлен.'}, status=status.HTTP_200_OK)

