from django.db import models
from user.models import User


class Event(models.Model):
    title = models.CharField(max_length=40, blank=False)
    description = models.CharField(max_length=255)
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_users = models.ManyToManyField(User, related_name='registered_events', blank=True)

    def __str__(self):
        return self.title
