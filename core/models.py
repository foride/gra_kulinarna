from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)  # Assuming the URL is optional
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_code = models.IntegerField()
    comment = models.TextField(max_length=255, null=True, blank=True)


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    creation_date = models.DateField()


class Ranking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField(unique=True)
    points = models.IntegerField()


class Achievement(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    points_required = models.IntegerField()

    # Assuming a Many-to-Many relationship with User
    users = models.ManyToManyField(User, through='UserAchievement')


class UserAchievement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
