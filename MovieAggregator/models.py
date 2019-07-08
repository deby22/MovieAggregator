from django.db import models

from .managers import MovieManager


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    rated = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    rated = models.CharField(max_length=255)
    released = models.DateField()
    runtime = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    plot = models.TextField()
    language = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    awards = models.CharField(max_length=255)
    poster = models.CharField(max_length=255)
    metascore = models.CharField(max_length=255)
    imdbrating = models.DecimalField(max_digits=3, decimal_places=2)
    imdbvotes = models.CharField(max_length=255)
    imdbid = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    dvd = models.CharField(max_length=255)
    boxoffice = models.CharField(max_length=255)
    production = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    objects = MovieManager()

    def __str__(self):
        return '{}. {} ({})'.format(self.pk, self.title, self.year)


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    source = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
