from code_service.libs.response import send_500
from code_service.logger.logging import setup_logger

logger = setup_logger(__name__)


class ExceptionMiddleware:

    HEALTH_CHECK_PATH = "/api/health-check"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path
        if self.HEALTH_CHECK_PATH not in path:
            logger.info(
                "Request: {} ,\n Headers: {} \n Body params: {} \n Query params: {}".format(
                    request.path, request.headers, request.body, request.GET
                )
            )
        response = self.get_response(request)

        if self.HEALTH_CHECK_PATH not in path:
            logger.info(
                "Response to request: {}: {}".format(request.path, response.content)
            )
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        logger.critical("Exception: {}".format(exception), exc_info=True)
        return send_500(
            {
                "code": "GENERAL_EXCEPTION",
                "message": "Something went wrong. We are working on it",
            }
        )
