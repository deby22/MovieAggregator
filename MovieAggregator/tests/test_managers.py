from datetime import datetime, timedelta

from django.test import TestCase

from MovieAggregator.external_api import Api
from MovieAggregator.models import Comment, Movie
from MovieAggregator.serializers import MovieSerializer
from MovieAggregator.utils import prepare_date


class MovieManagerTestCase(TestCase):
    def setUp(self):
        """Create movies."""
        title_list = ["avatar", "It", "Titanic"]
        self.movies = self.__create_movies(title_list)

    def __create_movies(self, title_list):
        """Fetch sample movies using API"""
        api = Api()
        movies = []
        for title in title_list:
            serializer = MovieSerializer(data=api.get(title))
            serializer.is_valid()
            movies.append(serializer.save())

        return movies

    def tearDown(self):
        """Remove created data."""
        for movie in self.movies:
            movie.delete()

    def test_ordering_without_date(self):
        comments = [10, 5, 2]
        for index, comment in enumerate(comments):
            for a in range(comment):
                Comment.objects.create(content="sample", movie=self.movies[index])

        total_comments = Movie.objects.top().values_list("total_comments", flat=True)
        self.assertEqual(list(total_comments), comments)

    def test_ordering_with_start_date(self):
        start_date = "2010-05-08T21:36:07"
        date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")

        # 10 comments in past
        for a in range(10):
            past = date - timedelta(days=1)
            comment = Comment.objects.create(content="sample", movie=self.movies[0])
            comment.created_at = past
            comment.save()

        # 5 comments current
        for a in range(5):
            comment = Comment.objects.create(content="sample", movie=self.movies[0])
            comment.created_at = date
            comment.save()

        total_comments = Movie.objects.top(start_date).values_list(
            "total_comments", flat=True
        )
        self.assertEqual(max(list(total_comments)), 5)

    def test_ordering_with_end_date(self):
        end_date = "2020-05-08T21:36:07"
        date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")

        # 10 comments in future
        for a in range(10):
            future = date + timedelta(days=1)
            comment = Comment.objects.create(content="sample", movie=self.movies[0])
            comment.created_at = future
            comment.save()

        # 5 comments current
        for a in range(5):
            comment = Comment.objects.create(content="sample", movie=self.movies[0])
            comment.created_at = date
            comment.save()

        total_comments = Movie.objects.top(None, end_date).values_list(
            "total_comments", flat=True
        )
        self.assertEqual(max(list(total_comments)), 5)

    def test_ordering_with_start_date_and_end_date(self):

        start_date = "2010-05-08T21:36:07"
        end_date = "2020-05-08T21:36:07"

        _start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        _end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")

        # 10 comments in future
        for a in range(10):
            future = _end_date + timedelta(days=1)
            comment = Comment.objects.create(content="sample", movie=self.movies[0])
            comment.created_at = future
            comment.save()

        # 10 comments in past
        for a in range(10):
            past = _start_date - timedelta(days=1)
            comment = Comment.objects.create(content="sample", movie=self.movies[0])
            comment.created_at = past
            comment.save()

        # 5 comments current
        for a in range(5):
            comment = Comment.objects.create(content="sample", movie=self.movies[0])
            comment.created_at = _start_date
            comment.save()

        total_comments = Movie.objects.top(start_date, end_date).values_list(
            "total_comments", flat=True
        )
        self.assertEqual(max(list(total_comments)), 5)
