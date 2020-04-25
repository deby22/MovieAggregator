from unittest.mock import Mock, patch

from django.test import TestCase
from requests.exceptions import ConnectionError

from MovieAggregator.exceptions import (ExternalApiConnectionError,
                                        MovieDoesNotExists)
from MovieAggregator.external_api import Api


class ApiTestCase(TestCase):
    @patch("MovieAggregator.external_api.requests")
    def test_get_with_connection_error(self, requests):
        requests.get.side_effect = ConnectionError

        api = Api()
        with self.assertRaises(ExternalApiConnectionError):
            api.get("title")

    @patch("MovieAggregator.external_api.requests")
    def test_get_without_movie(self, requests):
        response = Mock()
        response.json.return_value = {"error": "error message"}
        requests.get.return_value = response

        api = Api()
        with self.assertRaises(MovieDoesNotExists):
            api.get("title")

    @patch("MovieAggregator.external_api.requests")
    def test_get_with_sample_data(self, requests):
        response = Mock()
        data = {"title": "Avatar", "year": 2019, "genre": "Crime, Drama"}
        response.json.return_value = data
        requests.get.return_value = response

        api = Api()
        self.assertEqual(data, api.get("title"))
