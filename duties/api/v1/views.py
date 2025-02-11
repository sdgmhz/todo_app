from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
import requests


from .serializer import DutyModelSerializer, WeatherSerializer
from ...models import Duty
from .paginations import DutyPagination

"""model viewset for implement CRUD for duties"""


class DutyModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DutyModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"done_status": ["exact"], "deadline_date": ["gt", "lt"]}
    search_fields = ["title", "description"]
    ordering_fields = ["done_status", "deadline_date"]
    pagination_class = DutyPagination
    queryset = Duty.objects.all()

    """ override get_queryset method in order to each user could see only his/her own duties"""

    # def get_queryset(self):
    #     return Duty.objects.filter(author__user__id=self.request.user.id)


@method_decorator(cache_page(60), name="dispatch")
class WeatherCacheApiView(GenericAPIView):
    serializer_class = WeatherSerializer

    def get(self, request):
        data = {
            "detail": "Please enter the latitude and longitude of your desired location."
            "Note that latitude should be between +90 and -90 and longitude between +180 and -180 "
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create the url with geographic coordinates.It's better to not to share the API key in the code, but it's just a practice
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={serializer.validated_data["latitude"]}&lon={serializer.validated_data["longitude"]}&appid=9ac1c0c8e1403216448cb7a1437bac84'
        response = requests.get(url)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Failed to fetch weather data"}, status=response.status_code
            )
