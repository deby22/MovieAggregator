from django.db import models
from django.db.models import Count, Q


class MovieManager(models.Manager):

    def top(self, start_date=None, end_date=None):
        queryset = self.get_queryset()

        if start_date and end_date:
            return queryset.annotate(total_comments=Count('comment', filter=Q(comment__created_at__gte=start_date)&Q(comment__created_at__lte=end_date), distinct=True))

        if start_date and not end_date:
            return queryset.annotate(total_comments=Count('comment', filter=Q(comment__created_at__gte=start_date), distinct=True))

        if not start_date and end_date:
            return queryset.annotate(total_comments=Count('comment', filter=Q(comment__created_at__lte=end_date), distinct=True))

        return queryset.annotate(total_comments=Count('comment')).order_by('-total_comments')
