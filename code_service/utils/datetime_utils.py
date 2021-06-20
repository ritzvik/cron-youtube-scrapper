import pytz
from django.utils import timezone
from django.utils.timezone import make_aware

UTC_TZ = "UTC"


def get_present_datetime_in_utc():
    return timezone.now().astimezone(pytz.timezone(UTC_TZ))
