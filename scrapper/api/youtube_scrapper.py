from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from code_service.libs.response import send_200, send_400
from code_service.constants import DEFAULT_ITEMS_PER_PAGE, DEFAULT_PAGE_NUMBER
from scrapper.entity_member_functions import YoutubeScrapperService


class YoutubeVideo(APIView):

    class YoutubeVideoGetSerailizer(Serializer):
        items = serializers.IntegerField(min_value=1, default=DEFAULT_ITEMS_PER_PAGE)
        page = serializers.IntegerField(min_value=1, default=DEFAULT_PAGE_NUMBER)
        q = serializers.CharField(max_length=200, allow_null=True, allow_blank=True, default=None)

        def validate(self, data):
            paginated_res = Paginator(YoutubeScrapperService.get_youtube_results(search_string=data['q']), per_page=data['items'])
            max_pages = paginated_res.num_pages
            if data['page'] > max_pages:
                raise serializers.ValidationError("Max page number that can be requested is {}".format(max_pages))
            self.paginated_res = paginated_res
            return data

        def to_representation(self, data):
            paginated_res = self.paginated_res
            results = paginated_res.page(number=data['page'])
            lizt = list()
            for r in results:
                lizt.append({
                    'etag': r.etag,
                    'id':{'videoId': r.video_id},
                    'publishedAt': r.published_at.isoformat(),
                    'title': r.title,
                    'description': r.description,
                    'snippet': r.meta
                })
            return {'data': lizt, 'page': data['page'], 'items': data['items'], 'last_page': paginated_res.num_pages}

        def extract_error_msg(self):
            errors = self.errors
            for key, msg in errors.items():
                return str(msg[0])
            return "Error in fetching results"

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("items", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter("q", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
    )
    def get(self, request):
        q_params = request.query_params
        ser = self.YoutubeVideoGetSerailizer(data=q_params)
        if ser.is_valid(raise_exception=False):
            return send_200(data=ser.data, message="results retrieved successfully")
        else:
            return send_400(status="FAILURE", data={'errors': ser.errors}, message=ser.extract_error_msg())
