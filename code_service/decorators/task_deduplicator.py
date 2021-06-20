from functools import wraps
from code_service import caches
from code_service.logger.logging import setup_logger

log = setup_logger(__name__)


def task_deduplicator(function):
    """
    Task deduplicator for celery tasks
    """

    @wraps(function)
    def wrap(*args, **kwargs):
        cache_key = f"deduplicated_{function.__name__}_running"

        if caches.has_key(cache_key) and caches.get(cache_key):
            log.info(f"[task_deduplicator]: {function.__name__} rejected")
            return None

        log.info(f"[task_deduplicator]: {function.__name__} accepted")
        caches.set(cache_key, True, caches.ONE_MINUTE)
        try:
            return_val = function(*args, **kwargs)
            caches.set(cache_key, False, caches.ONE_MINUTE)
        except Exception as ex:
            caches.set(cache_key, False, caches.ONE_MINUTE)
            raise type(ex)(
                f"[task_deduplicator] rethrowing exception, message: {ex.args}"
            ).with_traceback(ex.__traceback__)

        return return_val

    wrap.__name__ = function.__name__
    return wrap
