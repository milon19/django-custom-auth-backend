from datetime import timedelta

from config.settings import config

DEFAULTS = {
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_HEADER_TYPE": "TOKEN",
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7)
}


class APISetting:
    def __init__(self):
        self.settings = self.get_authentication_setting()
        self.defaults = DEFAULTS

    @staticmethod
    def get_authentication_setting():
        settings = {
            "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
            "AUTH_HEADER_TYPE": config.AUTH_HEADER_TYPE,
        }
        return settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Attribute not found: '%s'" % attr)

        try:
            val = self.settings[attr]
        except KeyError:
            val = self.defaults[attr]

        setattr(self, attr, val)
        return val


api_settings = APISetting()
