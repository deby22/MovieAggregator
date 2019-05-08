from .models import Movie, Comment

from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class BasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
