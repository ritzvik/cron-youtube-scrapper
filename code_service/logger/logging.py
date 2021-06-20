import os
import logging
from inspect import currentframe
from logging.config import dictConfig

log_dir = "logs/"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": '"time": "{asctime}", "module": "{name}", "message": "{message}"',
            "style": "{",
        },
        "api_log_formatter": {
            "format": '"time": "{asctime}", "request_id": "{request_id}", '
            '"module": "{name}", "message": "{message}"',
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "request_id": {
            "()": "code_service.middleware.logger_middleware.RequestIdFilter"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_id"],
            "formatter": "api_log_formatter",
        },
        "celery": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "celery.log",
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"{log_dir}log",
            "filters": ["request_id"],
            "formatter": "api_log_formatter",
        },
    },
    "root": {"handlers": ["console", "file"], "level": "INFO"},
    "loggers": {
        "celery": {
            "handlers": ["celery", "console"],
            "level": "DEBUG",
            "propogate": True,
        },
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "formatter": "verbose",
        },
    },
}

dictConfig(LOGGING_CONFIG)


def setup_logger(module_name):
    return logging.getLogger(module_name)
