from django.db import models
from django.db.models import Count, Q

from datetime import datetime


class MovieManager(models.Manager):

    def top(self, start_date=None, end_date=None):
        queryset = self.get_queryset()

        # prepare date
        start_date = self.__prepare_date(start_date)
        end_date = self.__prepare_date(end_date)

        if start_date and end_date:
            return queryset.annotate(total_comments=Count('comment', filter=Q(comment__created_at__gte=start_date)&Q(comment__created_at__lte=end_date), distinct=True))

        if start_date and not end_date:
            return queryset.annotate(total_comments=Count('comment', filter=Q(comment__created_at__gte=start_date), distinct=True))

        if not start_date and end_date:
            return queryset.annotate(total_comments=Count('comment', filter=Q(comment__created_at__lte=end_date), distinct=True))

        return queryset.annotate(total_comments=Count('comment')).order_by('-total_comments')


    def __prepare_date(self, date):
        try:
            return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S') if date else None
        except ValueError:  # invalid dateformat
            return None
