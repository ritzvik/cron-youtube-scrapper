import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_RETRIES = 3


def requests_retry_session(
    retries=MAX_RETRIES, backoff_factor=0.5, session=None,
):
    if session is None:
        session = requests.Session()
    retry = Retry(
        total=retries, read=retries, connect=retries, backoff_factor=backoff_factor,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
