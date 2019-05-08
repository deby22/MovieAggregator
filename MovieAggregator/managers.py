from django.db import models
from django.db.models import Count


class MovieManager(models.Manager):

    def top(self):
        queryset = self.get_queryset()
        return queryset.annotate(total_comments=Count('comment')).order_by('-total_comments')
