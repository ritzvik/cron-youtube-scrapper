from http import HTTPStatus
from datetime import datetime
from typing import Optional

from django.db.models.query import QuerySet
from django.db.models import Q

from scrapper.models import YoutubeVideo
from external_service.remote_calls.youtube import GetYoutubeSearchResults

class YoutubeScrapperService:
    @staticmethod
    def store_youtube_results() -> Optional[QuerySet]:
        status_code, data = GetYoutubeSearchResults.get_responses()
        if status_code != HTTPStatus.OK:
            return None
        
        insert_models = list()
        video_ids = [item['id']['videoId'] for item in data['items']]
        existing_ids = set(YoutubeVideo.objects.filter(video_id__in=video_ids).values_list('video_id', flat=True))
        for item in data['items']:
            video_id = item['id']['videoId']
            if video_id in existing_ids:
                continue
            insert_models.append(
                YoutubeVideo(
                    etag = item['etag'],
                    video_id=video_id,
                    published_at=datetime.fromisoformat(item['snippet']['publishedAt'].replace('Z','+00:00', 1)),
                    title=item['snippet']['title'][:1000],
                    description=item['snippet']['description'][:5000],
                    meta = item['snippet'],
                )
            )
        return YoutubeVideo.objects.bulk_create(insert_models)

    @staticmethod
    def get_youtube_results(search_string: Optional[str] = None) -> QuerySet:
        if search_string is not None:
            search_string = search_string.lower()
            string_query = Q(title__icontains=search_string) | Q(description__icontains=search_string)
        else:
            string_query = Q()
        objs = YoutubeVideo.objects.filter(string_query).order_by('-published_at')
        return objs
