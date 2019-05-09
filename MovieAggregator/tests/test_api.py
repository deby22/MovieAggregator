from django.test import TestCase

from rest_framework.test import APIClient

from MovieAggregator.models import Movie
from MovieAggregator.serializers import MovieSerializer


class ApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Movie.objects.all().delete()

    def test_create_object(self):
        # Arrange
        title = 'Avengers'

        # Act
        response = self.client.post('/movie/', {'title': title}, format='json')

        # Assert
        data = response.json()
        movie = Movie.objects.get(pk = data['id'])
        serializer = MovieSerializer(instance=movie)
        self.assertEqual(serializer.data, data)
