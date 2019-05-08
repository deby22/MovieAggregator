from django_filters import rest_framework as filters

from rest_framework import serializers
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Comment
from .serlializers import (
    BasicSerializer,
    CommentSerializer,
    MovieSerializer,
    TopMovieSerializer,
)
from .external_api import Api
from .exceptions import ExternalApiConnectionError, MovieDoesNotExists


class TopMovieList(ListAPIView):
    '''Movie List aggregate data by comments count'''

    serializer_class = TopMovieSerializer
    queryset = Movie.objects.top()
    filter_backends = (filters.DjangoFilterBackend)
    filter_fields = ('movie', )


class MovieList(APIView):
    '''
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
    '''

    serializer_class = BasicSerializer
    extended_serializer = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', 'year', 'genre')
    filter_fields = ('title', 'writer', 'actors', 'plot')
    ordering_fields = ('title', 'year', 'metascore', 'released', 'dvd')

    def get_queryset(self):
        queryset = Movie.objects.all()
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def __get_data(self, title):
        '''Fetch data from external api.'''
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
        '''
            Two-stop validation process:
                First validate title send by user
                Second validate data from external api
        '''
        # pre_valid
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        # valid
        extended_serializer = self.extended_serializer(data=self.__get_data(data['title']))
        if extended_serializer.is_valid():
            extended_serializer.save()
            return Response(extended_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(ListCreateAPIView):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('id', )
