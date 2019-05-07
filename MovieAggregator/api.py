from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie
from .serlializers import BasicSerializer, MovieSerializer

from .external_api import Api


class MovieList(APIView):
    serializer = BasicSerializer
    extended_serializer = MovieSerializer

    def __get_data(self, title):
        api = Api()
        return api.get(title)


    def get(self, request, format=None):
        data = Movie.objects.all()
        serializer = self.extended_serializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # pre_valid
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        # valid
        extended_serializer = self.extended_serializer(data=self.__get_data(data['title']))
        if extended_serializer.is_valid():
            extended_serializer.save()
            return Response(extended_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
