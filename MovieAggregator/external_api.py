import requests
from requests.exceptions import ConnectionError

from .exceptions import ExternalApiConnectionError


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
            raise ExternalApiConnectionError('ConnectionError with OmdbAPI')
        else:
            return self.__map_json(response.json())

    def __map_json(self, data):
        '''Map json keys to lowwerkeys.'''
        return dict((k.lower(), v) for k, v in data.items())
