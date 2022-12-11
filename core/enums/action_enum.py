from datetime import timedelta
from enum import Enum


class ActionEnum(Enum):
    ACTIVATE = ('activate', timedelta(days=1))
    RESET_PASSWORD = ('reset_password', timedelta(days=1))

    def __init__(self, token_type, lifetime):
        self.lifetime = lifetime
        self.token_type = token_type
