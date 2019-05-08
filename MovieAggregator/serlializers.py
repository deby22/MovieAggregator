from .models import Movie, Comment, Rating

from rest_framework import serializers


class RatingSerializer(serializers.ModelSerializer):
    Source = serializers.CharField(source='source')
    Value = serializers.CharField(source='value')

    class Meta:
        model = Rating
        fields = ('Source', 'Value')


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        ratings = validated_data.pop('ratings')
        movie = Movie.objects.create(**validated_data)
        for rating in ratings:
            Rating.objects.create(movie=movie, **rating)
        return movie


class BasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', )


class TopMovieSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('title', 'total_comments', 'rank')

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
