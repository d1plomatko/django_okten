from typing import Type

from rest_framework_simplejwt.tokens import BlacklistMixin, Token

from rest_framework.generics import get_object_or_404

from apps.users.models import UserModel

from core.enums.action_enum import ActionEnum
from core.exceptions.jwt_exception import JWTException

TokenClass = Type[BlacklistMixin | Token]


class ActivateToken(BlacklistMixin, Token):
    lifetime = ActionEnum.ACTIVATE.lifetime
    token_type = ActionEnum.ACTIVATE.token_type


class ResetPasswordToken(BlacklistMixin, Token):
    lifetime = ActionEnum.RESET_PASSWORD.lifetime
    token_type = ActionEnum.RESET_PASSWORD.token_type


class JWTService:

    @staticmethod
    def create_token(user, token_class: TokenClass):
        return token_class.for_user(user)

    @staticmethod
    def validate_token(token, token_class: TokenClass):
        try:
            token_res = token_class(token)
            token_res.check_blacklist()
        except (Exception,):
            raise JWTException
        token_res.blacklist()
        user_id = token_res.payload.get('user_id')
        return get_object_or_404(UserModel, pk=user_id)
