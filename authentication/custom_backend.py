from django.contrib.auth import get_user_model

from rest_framework import authentication, HTTP_HEADER_ENCODING
from rest_framework.exceptions import AuthenticationFailed

from authentication.tokens import AccessToken
from authentication.settings import api_settings


class CustomJWTAuthenticationBackend(authentication.BaseAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        prefix, raw_token = self.get_auth_header_and_raw_token(header)
        if raw_token is None or prefix is None:
            return None
        validated_token = AccessToken(raw_token)
        return self.get_user(validated_token), validated_token

    @staticmethod
    def get_header(request):
        header = request.META.get(api_settings.AUTH_HEADER_NAME)
        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    @staticmethod
    def get_auth_header_and_raw_token(header):
        auth_header = header.split()
        if len(auth_header) == 0:
            return None, None

        if auth_header[0] != api_settings.AUTH_HEADER_TYPE:
            return None, None

        if len(auth_header) != 2:
            raise AuthenticationFailed("Authorization header must contain two space-delimited values")

        return auth_header[0], auth_header[1]

    def get_user(self, validated_token):
        try:
            user_id = validated_token["id"]
        except KeyError:
            raise AuthenticationFailed("Token contained no recognizable user identification")

        try:
            user = self.user_model.objects.get(id=user_id)
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        return user
