from calendar import timegm
from datetime import datetime

from django.conf import settings
from django.utils.timezone import is_naive, make_aware, utc


def make_utc(dt):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=utc)

    return dt


def aware_utcnow():
    return make_utc(datetime.utcnow())


def datetime_from_epoch(ts):
    return make_utc(datetime.utcfromtimestamp(ts))


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())
