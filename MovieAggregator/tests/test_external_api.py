from django.test import TestCase

from requests.exceptions import ConnectionError

from unittest.mock import patch, Mock

from MovieAggregator.exceptions import (
    ExternalApiConnectionError,
    MovieDoesNotExists,
)
from MovieAggregator.external_api import map_json, Api


class MapJsonTestCase(TestCase):

    def test_map_json(self):
        data = [
            ({'a': 'v'}, {'a': 'v'}),  # no change
            ({'A': 'v'}, {'a': 'v'}),  # lowercase
            ({'a': 'v', 'B': 'v'}, {'a': 'v', 'b': 'v'}),  # lowercase
            ({'A': 'V', 'B': ['v']}, {'a': 'V', 'b': ['v']}),  # lowercase
        ]
        for row in data:
            self.assertEqual(map_json(row[0]), row[1])


class ApiTestCase(TestCase):

    @patch('MovieAggregator.external_api.requests')
    def test_get_with_connection_error(self, requests):
        requests.get.side_effect = ConnectionError

        api = Api()
        with self.assertRaises(ExternalApiConnectionError):
            api.get('title')

    @patch('MovieAggregator.external_api.requests')
    def test_get_without_movie(self, requests):
        response = Mock()
        response.json.return_value = {'error': 'error message'}
        requests.get.return_value = response

        api = Api()
        with self.assertRaises(MovieDoesNotExists):
            api.get('title')

    @patch('MovieAggregator.external_api.requests')
    def test_get_with_sample_data(self, requests):
        response = Mock()
        data = {'title': 'Avatar', 'year': 2019, 'genre': 'Crime, Drama'}
        response.json.return_value = data
        requests.get.return_value = response

        api = Api()
        self.assertEqual(data, api.get('title'))


