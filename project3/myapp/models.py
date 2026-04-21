from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    LEVEL_CHOICES = [
        ('Elite', 'Elite'),
        ('Top', 'Top'),
        ('Mid', 'Mid'),
        ('Low', 'Low'),
    ]

    name = models.CharField(max_length=100)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    national_position = models.CharField(max_length=20, blank=True)
    club_position = models.CharField(max_length=20, blank=True)

    rating = models.IntegerField()
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField()

    skill_moves = models.IntegerField(null=True, blank=True)
    ball_control = models.IntegerField(null=True, blank=True)
    dribbling = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)

    player_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True)

    def __str__(self):
        return self.name

class WeatherRecord(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    temperature_max = models.FloatField(null=True, blank=True)
    temperature_min = models.FloatField(null=True, blank=True)
    precipitation_sum = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("city", "date")

    def __str__(self):
        return f"{self.city} - {self.date}"