from typing import Optional, Tuple
from simplejson.errors import JSONDecodeError as SimpleJSONDecodeError
from json.decoder import JSONDecodeError
from datetime import timedelta
from django.conf import settings

from external_service.remote_calls.requests_session import requests_retry_session
from code_service import constants
from code_service.utils.datetime_utils import get_present_datetime_in_utc
from code_service.logger.logging import setup_logger

log = setup_logger(__name__)

class GetYoutubeSearchResults:

    @staticmethod
    def get_api_endpoint() -> str:
        return "https://www.googleapis.com/youtube/v3/search"

    @staticmethod
    def get_headers() -> dict:
        return {

        }

    @staticmethod
    def get_query_params() -> dict:
        return {
            'part': 'snippet',
            'maxResults': '50',
            'type': 'video',
            'order': 'date',
            'publishedAfter': (get_present_datetime_in_utc()-timedelta(days=30)).isoformat(),
            'key': 'AIzaSyCJfuTB9QpX9RE2VYjr9eDbW-VnuW89-jU',
            'q': 'FamPay',
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
            try:
                response_json = response_data.json()
                log.info(f"*** Youtube API returned the response: {response_json} ***")
                return response_data.status_code, response_json
            except (SimpleJSONDecodeError, JSONDecodeError):
                return response_data.status_code, dict()
        except Exception as e:
            log.critical("Error in Youtube API {}".format(e), exc_info=True)
        return None, None
