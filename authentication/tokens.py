import jwt

from authentication.settings import api_settings
from config.settings import config
from authentication.expections import TokenError, TokeDecodeError
from authentication.utils import aware_utcnow, datetime_to_epoch


class Token:
    token_type = None
    lifetime = None

    def __init__(self, token):
        if self.token_type is None or self.lifetime is None:
            raise TokenError("Token type or lifetime is required")
        self.token = token  # NOSONAR
        self.current_time = aware_utcnow()

        if token is not None:
            try:
                self.payload = self.decode(token)
            except TokeDecodeError:
                raise TokenError("Token is invalid or expired")

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    @staticmethod
    def decode(token):
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET,
                algorithm='HS256',
            )
        except Exception:
            raise TokeDecodeError("Token is invalid or expired")


class AccessToken(Token):
    token_type = "access"
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME
