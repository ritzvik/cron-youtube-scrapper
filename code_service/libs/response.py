from django.http.response import JsonResponse


def _send(data, status_code, safe=True):
    return JsonResponse(data=data, status=status_code, safe=safe)


def send_200(data, message=""):
    data["status_code"] = 200
    if message:
        data["message"] = message
    return _send(data, 200)


def send_400(status, data={}, message=""):
    if not data:
        data = {}
    data["status"] = status
    data["status_code"] = 400
    if message:
        data["message"] = message
    return _send(data, 400)


def send_500(data):
    data["status_code"] = 500
    return _send(data, 500)
