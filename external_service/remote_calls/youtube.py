from http import HTTPStatus
from typing import Optional, Tuple
from simplejson.errors import JSONDecodeError as SimpleJSONDecodeError
from json.decoder import JSONDecodeError
from datetime import timedelta
from django.conf import settings

from external_service.remote_calls.requests_session import requests_retry_session
from code_service import constants
from code_service.utils.datetime_utils import get_present_datetime_in_utc
from code_service.logger.logging import setup_logger
from code_service import caches

log = setup_logger(__name__)


class GetYoutubeSearchResults:
    @staticmethod
    def get_api_endpoint() -> str:
        return "https://www.googleapis.com/youtube/v3/search"

    @staticmethod
    def get_headers() -> dict:
        return {}

    @staticmethod
    def get_api_key_index() -> int:
        last_status_redis_key = "LAST_YOUTUBE_STATUS_CODE"
        last_index_key = "LAST_YOUTUBE_KEY_INDEX"
        if caches.get(last_status_redis_key) == HTTPStatus.FORBIDDEN:
            last_index = caches.get(last_index_key) or 0
            log.info(f"last index was {last_index}")
            caches.set(
                last_index_key,
                (last_index + 1) % len(settings.YOUTUBE_KEYS),
                duration=caches.HALF_HOUR,
            )
            log.info(f"switching API key to index {caches.get(last_index_key)}")
        return caches.get(last_index_key) or 0

    @staticmethod
    def set_last_status(status_code: int) -> None:
        log.info(f"setting last status code {status_code}")
        last_status_redis_key = "LAST_YOUTUBE_STATUS_CODE"
        caches.set(last_status_redis_key, status_code, duration=caches.HALF_HOUR)

    @staticmethod
    def get_query_params() -> dict:
        log.info(f"youtube API keys {settings.YOUTUBE_KEYS}")
        return {
            "part": "snippet",
            "maxResults": "50",
            "type": "video",
            "order": "date",
            "publishedAfter": (
                get_present_datetime_in_utc() - timedelta(days=30)
            ).isoformat(),
            "key": settings.YOUTUBE_KEYS[GetYoutubeSearchResults.get_api_key_index()],
            "q": settings.YOUTUBE_QUERY_STRING,
        }

    @classmethod
    def get_responses(cls) -> Tuple[Optional[int], Optional[dict]]:
        try:
            response_data = requests_retry_session(retries=3).get(
                url=cls.get_api_endpoint(),
                headers=cls.get_headers(),
                params=cls.get_query_params(),
            )
            log.info(
                f"Youtube API returned code: {response_data.status_code}, response: {response_data}"
            )
            cls.set_last_status(int(response_data.status_code))
            try:
                response_json = response_data.json()
                log.info(f"*** Youtube API returned the response: {response_json} ***")
                return response_data.status_code, response_json
            except (SimpleJSONDecodeError, JSONDecodeError):
                return response_data.status_code, dict()
        except Exception as e:
            log.critical("Error in Youtube API {}".format(e), exc_info=True)
        return None, None
