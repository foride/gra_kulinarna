from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Coalesce

from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    visit_code = models.CharField(max_length=4)
    open_hours = models.CharField(max_length=255)
    localization = models.CharField(max_length=400)
    iframe_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_code = models.IntegerField()
    comment = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.venue.name} - {self.visit_date}'


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    creation_date = models.DateField()

    def __str__(self):
        return f'Discussion by {self.user.username} on {self.venue.name}'


class Ranking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    position = models.IntegerField(unique=True, null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"


class Achievement(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    points_required = models.IntegerField()
    users = models.ManyToManyField(User, through='UserAchievement')

    def __str__(self):
        return self.name

    @classmethod
    def total_achievements_count(cls):
        return cls.objects.count()


class UserAchievement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acquisition_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name}'

    @staticmethod
    def achievements_count_for_user(user):
        return UserAchievement.objects.filter(user=user).count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_venues = models.ManyToManyField(Venue, related_name='favorited_by')

    def user_ranking(self):
        # Subquery to get points from the Ranking model
        ranking_points_subquery = Ranking.objects.filter(user=OuterRef('user')).values('points')

        # Annotate user profiles with their total points using Subquery and Coalesce to handle users without points
        user_profiles = UserProfile.objects.annotate(
            total_points=Coalesce(Subquery(ranking_points_subquery[:1]), Value(0))
        ).order_by('-total_points')

        # Calculate and return the rank of the current user
        for rank, user_profile in enumerate(user_profiles, start=1):
            if user_profile.user == self.user:
                return rank
        return UserProfile.objects.count()  # Default rank if not found in the sorted list

    def __str__(self):
        return self.user.username
