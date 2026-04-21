from django.contrib import admin
from .models import Country, Team, Player
from .models import WeatherRecord

admin.site.register(WeatherRecord)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'team', 'nationality', 'rating', 'age', 'player_level']
    search_fields = ['name', 'team__name', 'nationality__name']
    list_filter = ['team', 'nationality', 'player_level']

