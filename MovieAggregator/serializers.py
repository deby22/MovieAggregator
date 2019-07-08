from .models import Movie, Comment, Rating

from rest_framework import serializers

MIN_YEAR = 0
MAX_YEAR = 2100


class RatingSerializer(serializers.ModelSerializer):
    Source = serializers.CharField(source='source')
    Value = serializers.CharField(source='value')

    class Meta:
        model = Rating
        fields = ('Source', 'Value')


class MovieSerializer(serializers.ModelSerializer):
    Actors = serializers.CharField(max_length=255, source='actors')
    Awards = serializers.CharField(max_length=255, source='awards')
    BoxOffice = serializers.CharField(max_length=255, source='boxoffice')
    Country = serializers.CharField(max_length=255, source='country')
    DVD = serializers.CharField(max_length=255, source='dvd')
    Director = serializers.CharField(max_length=255, source='director')
    Genre = serializers.CharField(max_length=255, source='genre')
    Language = serializers.CharField(max_length=255, source='language')
    Metascore = serializers.CharField(max_length=255, source='metascore')
    Plot = serializers.CharField(style={'base_template': 'textarea.html'}, source='plot')
    Poster = serializers.CharField(max_length=255, source='poster')
    Production = serializers.CharField(max_length=255, source='production')
    Rated = serializers.CharField(max_length=255, source='rated')
    Released = serializers.DateField(source='released')
    Runtime = serializers.CharField(max_length=255, source='runtime')
    Title = serializers.CharField(max_length=255, source='title')
    Type = serializers.CharField(max_length=255, source='type')
    Website = serializers.CharField(max_length=255, source='website')
    Writer = serializers.CharField(max_length=255, source='writer')
    Year = serializers.IntegerField(min_value=MIN_YEAR, max_value=MAX_YEAR, source='year')
    imdbID = serializers.CharField(max_length=255, source='imdbid')
    imdbRating = serializers.DecimalField(max_digits=3, decimal_places=2, source='imdbrating')
    imdbVotes = serializers.CharField(max_length=255, source='imdbvotes')
    Ratings = RatingSerializer(many=True, source='ratings')

    class Meta:
        model = Movie
        fields = (
            'Actors', 'Awards', 'BoxOffice', 'Country', 'DVD', 'Director',
            'Genre', 'Language', 'Metascore', 'Plot', 'Poster', 'Production',
            'Rated', 'Released', 'Runtime', 'Title', 'Type', 'Website',
            'Writer', 'Year', 'imdbID', 'imdbRating', 'imdbVotes', 'Ratings',
        )

    def create(self, validated_data):
        '''Create Movie and nested Ratings.'''
        ratings = validated_data.pop('ratings', [])
        movie = Movie.objects.create(**validated_data)
        for rating in ratings:
            Rating.objects.create(movie=movie, **rating)

        return movie


class BasicSerializer(MovieSerializer):

    class Meta:
        model = Movie
        fields = ('title', )


class TopMovieSerializer(MovieSerializer):
    total_comments = serializers.IntegerField()
    rank = serializers.SerializerMethodField()
    movie_id = serializers.IntegerField(source='id')

    class Meta:
        model = Movie
        fields = ('movie_id', 'total_comments', 'rank')

    def get_rank(self, instance):
        '''
        Really bad idea.
        RowNumber or Rank is not suppported on sqlite3<=3.25.

        There is a lot of redundant request to datebase.

        Better way is add this line to manager:
            annotate(rank = Window(expression=RowNumber()))
        '''
        comments = instance.comment_set.count()
        queryset = Movie.objects.top().filter(total_comments__gte=comments)
        return queryset.values_list('total_comments').distinct().count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
