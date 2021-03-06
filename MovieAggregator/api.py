from django_filters import rest_framework as filters
from rest_framework import serializers, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import ExternalApiConnectionError, MovieDoesNotExists
from .external_api import Api
from .models import Comment, Movie
from .serializers import (
    BasicSerializer,
    CommentSerializer,
    MovieSerializer,
    TopMovieSerializer,
)


class TopMovieList(ListAPIView):
    """Movie List aggregate data by comments count in the date range

    Valid date format:
        %Y-%m-%dT%H:%M:%S

    Ranking by comments added after specyfic date:
        ?start_date=2010-05-08T21:36:07

    Ranking by comments added before specyfic date:
        ?end_date=2020-05-08T21:36:07

    Ranking by comments added between:
        start_date=2010-05-08T21:36:07&end_date=2020-05-08T21:36:07
    """

    serializer_class = TopMovieSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        return Movie.objects.top(start_date, end_date).order_by("-total_comments", "id")


class MovieList(APIView):
    """
        List and Create Movie API.

        List:
            search by most common field:
                title, year and genre

            filter by specific fields:
                title, writer, actors and plot

            ordering by
                title, year, metascore, released, and dvd

        Create:
            Based on passed title, other details is fetched from external API
    """

    serializer_class = BasicSerializer
    extended_serializer = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("title", "year", "genre")
    filter_fields = ("title", "writer", "actors", "plot")
    ordering_fields = ("title", "year", "metascore", "released", "dvd")

    def get_queryset(self):
        queryset = Movie.objects.all()
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def __get_data(self, title):
        """Fetch data from external api."""
        api = Api()
        try:
            return api.get(title)
        except (ExternalApiConnectionError, MovieDoesNotExists) as e:
            raise serializers.ValidationError(e)

    def get(self, request, format=None):
        data = self.get_queryset()
        serializer = self.extended_serializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Two-stop validation process:
                First validate title send by user
                Second validate data from external api

            Data from external api stored in session to avoid redundant requests.
        """
        # cache external api result
        title = request.data.get("title")
        if not title in request.session:
            # pre_valid
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            prepared_data = serializer.data

            # valid
            data = self.__get_data(prepared_data["title"])
            request.session[title] = data
        else:
            data = request.session[title]

        extended_serializer = self.extended_serializer(data=data)
        if extended_serializer.is_valid(raise_exception=True):
            extended_serializer.save()
            return Response(extended_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(ListCreateAPIView):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ("movie",)
