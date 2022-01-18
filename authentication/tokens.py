import jwt

from authentication.settings import api_settings
from config.settings import config
from authentication.expections import TokenError, TokeDecodeError
from authentication.utils import aware_utcnow, datetime_to_epoch


class Token:
    token_type = None
    lifetime = None

    def __init__(self, token=None):
        if self.token_type is None or self.lifetime is None:
            raise TokenError("Token type or lifetime is required")
        self.token = token  # NOSONAR
        self.current_time = aware_utcnow()

        if token is not None:
            try:
                self.payload = self.decode(token)
            except TokeDecodeError:
                raise TokenError("Token is invalid or expired")
        else:
            self.payload = {"type": self.token_type}
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def set_exp(self, claim="exp", from_time=None, lifetime=None):
        if from_time is None:
            from_time = self.current_time
        if lifetime is None:
            lifetime = self.lifetime
        self.payload[claim] = datetime_to_epoch(from_time + lifetime)

    @classmethod
    def login(cls, user):
        user_id = user.id
        if not isinstance(user_id, int):
            user_id = str(user_id)
        token = cls()
        token["id"] = user_id
        return token

    @staticmethod
    def decode(token):
        try:
            return jwt.decode(token, config.JWT_SECRET, algorithms='HS256')
        except Exception:
            raise TokeDecodeError("Token is invalid or expired")

    def encode(self):
        jwt_payload = self.payload.copy()
        token = jwt.encode(jwt_payload, config.JWT_SECRET, algorithm='HS256')
        return token

    @property
    def get_token(self):
        return self.encode()


class AccessToken(Token):
    token_type = "access"
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME


class RefreshToken(Token):
    token_type = "refresh"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME

    @property
    def access_token(self):
        access = AccessToken()
        access.set_exp(from_time=self.current_time)
        return access.get_token
