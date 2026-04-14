from django.contrib import admin
from .models import Country, Team, Player


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']
    search_fields = ['name']
    list_filter = ['country']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'team', 'position', 'overall_rating', 'age']
    search_fields = ['name', 'nationality']
    list_filter = ['position', 'team']