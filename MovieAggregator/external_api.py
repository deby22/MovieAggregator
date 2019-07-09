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

        Sample result:
            {
				'Title': 'John Wick',
				'Year': '2014',
				'Rated': 'R',
				'Released': '24 Oct 2014',
				'Runtime': '101 min',
				'Genre': 'Action, Crime, Thriller',
				'Director': 'Chad Stahelski, David Leitch',
				'Writer': 'Derek Kolstad',
				'Actors': 'Keanu Reeves, Michael Nyqvist, Alfie Allen, Willem Dafoe',
                'Plot': 'An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.',
                'Language': 'English, Russian, Hungarian',
                'Country': 'China, USA',
                'Awards': '5 wins & 8 nominations.',
                'Poster': 'https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg',
                'Ratings': [
                    {'Source': 'Internet Movie Database', 'Value': '7.4/10'},
                    {'Source': 'Rotten Tomatoes', 'Value': '86%'},
                    {'Source': 'Metacritic', 'Value': '68/100'}],
                'Metascore': '68',
                'imdbRating': '7.4',
                'imdbVotes': '448,477',
                'imdbID': 'tt2911666',
                'Type': 'movie',
                'DVD': '03 Feb 2015',
                'BoxOffice': 'N/A',
                'Production': 'LionsGate Entertainment',
                'Website': 'http://johnwickthemovie.com/',
                'Response': 'True'
			}
    '''

    def __init__(self, url=API_URL):
        self.url = url

    def get(self, title):
        try:
            response = requests.get(self.url, params={'t': title})
        except ConnectionError as e:
            logger.error(e)
            raise ExternalApiConnectionError('ConnectionError with fetch data')
        else:
            data = response.json()
            if data.get('error'):
                raise MovieDoesNotExists('Movie not found!')

            return data

