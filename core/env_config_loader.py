import json


def init_config(os):
    return Config(os)


class Config:
    def __init__(self, os):
        self.os = os
        if self.os.getenv("DATABASES"):
            self.DATABASES = json.loads(self.os.getenv("DATABASES"))
        self.DEBUG = self.os.getenv("DEBUG", default=False)
        self.APP_SECRET = self.os.getenv("APP_SECRET",  default=None)