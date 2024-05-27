from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Venue(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField(unique=True)
    points = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.position}'


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
        user_rankings = UserProfile.objects.annotate(
            total_points=Sum('user__userachievement__achievement__points_required')
        ).order_by('-total_points')

        for rank, user_profile in enumerate(user_rankings, start=1):
            if user_profile.user == self.user:
                return rank
        return User.objects.count()  # Default rank if not found in the sorted list
