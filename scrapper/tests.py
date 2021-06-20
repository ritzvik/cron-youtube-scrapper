from external_service.remote_calls.youtube import GetYoutubeSearchResults
from django.test import TestCase
from uuid import uuid4
from datetime import datetime
from scrapper.models import YoutubeVideo
from scrapper.entity_member_functions import YoutubeScrapperService
from unittest.mock import patch, MagicMock

# Create your tests here.


def uuid4_str():
    return str(uuid4())


class TestYoutubeVideoService(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @patch.object(GetYoutubeSearchResults, "get_responses")
    def test_populate_youtube_videos_and_retrive_them(self, youtube_fetch: MagicMock):
        video_id = "AkffLs-sg0s"
        youtube_fetch.return_value = (
            200,
            {
                "kind": "youtube#searchListResponse",
                "etag": "W-8WTZdsPa3GIkrYg3ng5nOp_t0",
                "nextPageToken": "CAEQAA",
                "regionCode": "IN",
                "pageInfo": {"totalResults": 1000000, "resultsPerPage": 1},
                "items": [
                    {
                        "kind": "youtube#searchResult",
                        "etag": "BzdehT6egkxJJ4fUD36PQTu-Kuc",
                        "id": {"kind": "youtube#video", "videoId": video_id},
                        "snippet": {
                            "publishedAt": "2021-06-11T04:30:01Z",
                            "channelId": "UCMtFAi84ehTSYSE9XoHefig",
                            "title": "A Late Show Series Finale: Stephen Says Farewell To The Storage Closet",
                            "description": "That's it for A Late Show! Join Stephen Colbert in bidding a fond farewell to the storage closet set and the 15-month long quarantine edition of America's favorite ...",
                            "thumbnails": {
                                "default": {
                                    "url": "https://i.ytimg.com/vi/AkffLs-sg0s/default.jpg",
                                    "width": 120,
                                    "height": 90,
                                },
                                "medium": {
                                    "url": "https://i.ytimg.com/vi/AkffLs-sg0s/mqdefault.jpg",
                                    "width": 320,
                                    "height": 180,
                                },
                                "high": {
                                    "url": "https://i.ytimg.com/vi/AkffLs-sg0s/hqdefault.jpg",
                                    "width": 480,
                                    "height": 360,
                                },
                            },
                            "channelTitle": "The Late Show with Stephen Colbert",
                            "liveBroadcastContent": "none",
                            "publishTime": "2021-06-11T04:30:01Z",
                        },
                    }
                ],
            },
        )
        YoutubeScrapperService.store_youtube_results()
        objs = YoutubeScrapperService.get_youtube_results()
        assert objs[0].video_id == video_id

    def test_query_with_string(self):
        # create_models
        objs = [
            YoutubeVideo(
                etag=uuid4_str(),
                video_id=uuid4_str(),
                published_at=datetime.now(),
                title="How Tea is Good??",
                description="",
            ),
            YoutubeVideo(
                etag=uuid4_str(),
                video_id=uuid4_str(),
                published_at=datetime.now(),
                title="",
                description="Green Good Tea",
            ),
            YoutubeVideo(
                etag=uuid4_str(),
                video_id=uuid4_str(),
                published_at=datetime.now(),
                title="",
                description="Black tea",
            ),
        ]
        YoutubeVideo.objects.bulk_create(objs)
        new_objs = YoutubeScrapperService.get_youtube_results(
            search_string="good tea. "
        )
        assert len(new_objs) == 2
        assert new_objs[0].video_id in (objs[0].video_id, objs[1].video_id)
        assert new_objs[1].video_id in (objs[0].video_id, objs[1].video_id)
