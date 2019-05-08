import requests
from requests.exceptions import ConnectionError

from .exceptions import ExternalApiConnectionError, MovieDoesNotExists


OMDB_API_KEY = '8f6b5665'

API_URL = 'http://www.omdbapi.com/?apikey={}'.format(OMDB_API_KEY)


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
        except ConnectionError:
            # log info here
            raise ExternalApiConnectionError('ConnectionError with fetch data')
        else:
            data = self.__map_json(response.json())
            if data.get('error'):
                raise MovieDoesNotExists('Movie not found!')

            return data

    def __map_json(self, data):
        '''Map json keys to lowerkeys.'''
        return dict((k.lower(), v) for k, v in data.items())
