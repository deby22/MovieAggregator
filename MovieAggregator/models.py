from django.db import models

from .managers import MovieManager


class Movie(models.Model):
    title = models.CharField(max_length=255)
    rated = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    rated = models.CharField(max_length=255)
    released = models.CharField(max_length=255)   # DataField? "25 Jun 1982",
    runtime = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    plot = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    awards = models.CharField(max_length=255)
    poster = models.CharField(max_length=255)  # URLField?
    metascore = models.CharField(max_length=255)  # IntegerField?
    imdbrating = models.CharField(max_length=255)  # DoubleField?
    imdbvotes = models.CharField(max_length=255)  # DoubleField?
    imdbid = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    dvd = models.CharField(max_length=255)  # DataField? "27 Aug 1997",
    boxoffice = models.CharField(max_length=255)
    production = models.CharField(max_length=255)
    website = models.CharField(max_length=255)  # URLField

    objects = MovieManager()


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    source = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
