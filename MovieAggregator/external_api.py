from django.conf import settings

import requests
from requests.exceptions import ConnectTimeout


OMDB_API_KEY = '8f6b5665'

API_URL = 'http://www.omdbapi.com/?apikey={}'.format(OMDB_API_KEY)


class Api:

    def get(self, title):
        # what if film doesn't, exist
        url = API_URL + '&t=' + title
        try:
            response = requests.get(url)
        except ConnectTimeout:
            return {}
        else:
            return self.__map_json(response.json())

    def __map_json(self, data):
        '''Map json keys to lowwerkeys.'''
        return dict((k.lower(), v) for k, v in data.items())
