from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed


class TokenError(Exception):
    pass


class TokeDecodeError(Exception):
    pass


class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Token is invalid or expired"
    default_code = "token_not_valid"
