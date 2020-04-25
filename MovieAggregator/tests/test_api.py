from unittest.mock import Mock, patch

from django.test import TestCase
from rest_framework.serializers import ValidationError
from rest_framework.test import APIClient

from MovieAggregator.exceptions import (ExternalApiConnectionError,
                                        MovieDoesNotExists)
from MovieAggregator.models import Comment, Movie
from MovieAggregator.serializers import (CommentSerializer, MovieSerializer,
                                         TopMovieSerializer)


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Movie.objects.all().delete()

    def test_create_object(self):
        # Arrange
        title = "Avengers"

        # Act
        response = self.client.post("/movies/", {"title": title}, format="json")

        # Assert
        data = response.json()
        movie = Movie.objects.get(pk=data["ID"])
        serializer = MovieSerializer(instance=movie)
        self.assertEqual(serializer.data, data)

    def test_list_objects(self):
        # Arrange
        titles = ["Avengers", "Avatar", "Blade Runner"]
        for title in titles:
            self.client.post("/movies/", {"title": title}, format="json")

        # Act
        response = self.client.get("/movies/")
        data = response.json()
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        # Assert
        self.assertEqual(serializer.data, data)

    def test_top(self):
        # Arrange
        titles = ["Avengers", "Avatar", "Blade Runner"]
        for title in titles:
            self.client.post("/movies/", {"title": title}, format="json")

        self.client.post("/comments/", {"content": "Nice!", "movie": 1}, format="json")

        # Act
        response = self.client.get("/top/")
        data = response.json()
        movies = Movie.objects.top()
        serializer = TopMovieSerializer(movies, many=True)

        # Assert
        self.assertEqual(serializer.data, data)

    def test_list_comments(self):
        # Arrange
        title = "Avengers"
        commnets = ["OK", "Nice", "Amazing"]

        self.client.post("/movies/", {"title": title}, format="json")
        for comment in commnets:
            self.client.post(
                "/comments/", {"content": comment, "movie": 1}, format="json"
            )

        # Act
        response = self.client.get("/comments/")
        data = response.json()
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        # Assert
        self.assertEqual(serializer.data, data)

    @patch("MovieAggregator.api.Api")
    def test_raise_validationerror(self, api):
        # Arrange
        obj = Mock(side_effect=ExternalApiConnectionError)
        api().get = obj

        # Act
        response = self.client.post("/movies/", {"title": "title"}, format="json")

        # Assert
        self.assertEqual(response.status_code, 400)
