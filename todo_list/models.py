from django.conf import settings
from django.db import models

from datetime import datetime
from django.utils import timezone


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("Title", default="", max_length=255)
    description = models.TextField("Description", default="", blank=True)

    longestStreak = models.IntegerField("Longest Streak", default=0, blank=True)
    currentStreak = models.IntegerField("Current Streak", default=0, blank=True)
    streakSum = models.IntegerField("Streak Sum", default=0, blank=True)
    lastDate = models.DateTimeField("Last Date", auto_now_add=True, blank=True)
    isDoneToday = models.BooleanField("isDoneToday", default = False)

    streakOrNot = models.TextField(default="0,", blank=True)

    def __str__(self):
        return self.title
