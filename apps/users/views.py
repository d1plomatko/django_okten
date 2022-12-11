from abc import ABC, abstractmethod
from typing import Type

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.auto_parks.serializers import AutoParkSerializer
from apps.users.models import UserModel as User

from core.services.email_service import EmailService
from core.services.jwt_service import JWTService, ResetPasswordToken

from .permissions import IsSuperUser
from .serializers import AvatarSerializer, EmailSerializer, PasswordSerializer, UserSerializer

UserModel: Type[User] = get_user_model()


class UserCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class AdminTools(GenericAPIView, ABC):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id)

    @abstractmethod
    def patch(self, *args, **kwargs):
        pass


class SuperUserTools(AdminTools, ABC):
    permission_classes = (IsSuperUser,)


class UserActivateView(AdminTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserDeActivateView(AdminTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToAdmin(SuperUserTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUser(SuperUserTools):
    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AutoParkListCreateView(GenericAPIView):
    def get_object(self) -> User:
        return self.request.user

    def get(self, *args, **kwargs):
        auto_parks = self.get_object().auto_parks
        serializer = AutoParkSerializer(auto_parks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = AutoParkSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        serializer.save(user=user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class AddAvatarView(UpdateAPIView):
    serializer_class = AvatarSerializer
    http_method_names = ('patch',)

    def get_object(self):
        return self.request.user.profile


class ResetPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        email = self.request.data
        serializer = EmailSerializer(data=email)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, email=serializer.data.get('email'))
        EmailService.reset_password_email(user)
        return Response(status=status.HTTP_200_OK)


class SaveNewPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)

    def patch(self, *args, **kwargs):
        token = kwargs.get('token')
        user = JWTService.validate_token(token, ResetPasswordToken)
        password = self.request.data
        serializer = PasswordSerializer(data=password)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get('password'))
        user.save()
        return Response(status=status.HTTP_200_OK)
