import logging
import uuid
from threading import local

from rest_framework.authentication import get_authorization_header

_local = local()


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = "".join(str(uuid.uuid4()).split("-"))
        _local.request_id = request.id

        return self.get_response(request)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = ""

        if hasattr(_local, "request_id"):
            record.request_id = _local.request_id
        return True
