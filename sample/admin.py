from django.contrib import admin
from .models import Matches, Tournaments, Teams


@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    pass

@admin.register(Tournaments)
class TournamentsAdmin(admin.ModelAdmin):
    pass

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    pass