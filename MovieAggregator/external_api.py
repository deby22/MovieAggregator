import logging

import requests

from requests.exceptions import ConnectionError

from django.conf import settings

from .exceptions import ExternalApiConnectionError, MovieDoesNotExists

logger = logging.getLogger(__name__)

API_URL = 'http://www.omdbapi.com/?apikey={}'.format(settings.OMDB_API_KEY)


class Api:
    '''
        API to fetch data from OMDB.

        Raises:
            ConnectionError: passed from API
    '''

    def get(self, title):
        url = API_URL + '&t=' + title
        try:
            response = requests.get(url)
        except ConnectionError as e:
            logger.error(e)
            raise ExternalApiConnectionError('ConnectionError with fetch data')
        else:
            data = response.json()
            if data.get('error'):
                raise MovieDoesNotExists('Movie not found!')

            return data

