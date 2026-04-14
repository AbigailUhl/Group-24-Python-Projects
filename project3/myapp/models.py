from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    nationality = models.CharField(max_length=100, blank=True)
    overall_rating = models.IntegerField()
    potential = models.IntegerField()
    pace = models.IntegerField(null=True, blank=True)
    shooting = models.IntegerField(null=True, blank=True)
    passing = models.IntegerField(null=True, blank=True)
    dribbling = models.IntegerField(null=True, blank=True)
    defending = models.IntegerField(null=True, blank=True)
    physical = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name