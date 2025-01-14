from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime



class Venues(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Name")
    location = models.CharField(blank=True, null=True, verbose_name="Location")
    latitude = models.CharField(blank=True, null=True, verbose_name="Latitude")
    longitude = models.CharField(blank=True, null=True, verbose_name="Longitude")
    timezone_hr = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "venues"
        verbose_name = "Venue"
        verbose_name_plural = "Venues"

class MatchReferees(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Name")
    image = models.ImageField(upload_to='match_referees/', blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "match_referees"
        verbose_name = "Match Referee"
        verbose_name_plural = "Match Referees"

class MatchCoach(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Name")
    image = models.ImageField(upload_to='match_coaches/', blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "match_coaches"
        verbose_name = "Match Coach"
        verbose_name_plural = "Match Coaches"

class Teams(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Name")
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True, verbose_name="Logo")
    reference_id = models.CharField(max_length=250, null=True, blank=True, verbose_name="Reference id")
    merge_parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='parent_of', null=True, blank=True, verbose_name="Merge Parent")
    class MergeStatus(models.TextChoices):
        NEW = 'new', 'New'
        MERGE = 'merge', 'Merge'
    merge_status = models.CharField(max_length=150, null=True, blank=True, choices=MergeStatus.choices)
    status = models.BooleanField(default=True, verbose_name="Active Status")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    similar_count = models.FloatField(default=0, verbose_name="Similarity")
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.name

    def data_score(self):
        filled_fields = [field.name for field in self._meta.fields if getattr(self, field.name)]
        total_fields = len(self._meta.fields) - 1
        score = (len(filled_fields) / total_fields) * 10
        return round(score,1)

    class Meta:
        db_table = "teams"
        verbose_name = "Team"
        verbose_name_plural = "Teams"

class TournamentType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class TournamentEdition(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    logo = models.ImageField(upload_to='tournament/edition/', blank=True, null=True, verbose_name="Logo")
    triple_corona = models.BooleanField(default=False, verbose_name="Triple Corona")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Edition"
        verbose_name_plural = "Editions"

class Tournaments(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Name")
    PARTNER_TYPES = [
        ('1', 'polo_argentino'),
    ]
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True, verbose_name="Logo")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Start Date")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="End Date")
    winner = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, blank=True,related_name='tournament_winner_team')
    edition = models.ForeignKey(TournamentEdition, on_delete=models.CASCADE, null=True, blank=True, related_name='tournament_edition', verbose_name="Edition")
    is_open = models.BooleanField(default=False, verbose_name="Is Open")
    is_ranking = models.BooleanField(default=False, verbose_name="Is Ranking")
    win_point = models.IntegerField(null=True, blank=True, verbose_name="Points per win")
    show_matches =  models.BooleanField(default=True, verbose_name="Show in matches")
    partner = models.CharField(
        max_length=50,
        choices=PARTNER_TYPES,
        default='',
        blank=True,
        null=True,
        verbose_name="Partner")
    created_at = models.DateTimeField(auto_now_add=True)
    class Ranking(models.TextChoices):
        T = 'T', 'T'
        H = 'H', 'H'
        CAA = 'CAA', 'CAA'
        OTROS = 'OTROS', 'OTROS'
        TORTUGAS = 'TORTUGAS', 'TORTUGAS'
        HURLINGHAM = 'HURLINGHAM', 'HURLINGHAM'
        RV = 'RV', 'RV'
    ranking_name = models.CharField(max_length=150, null=True, blank=True,  choices=Ranking.choices, verbose_name="Ranking Name")


    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

class TournamentGroupTeams(models.Model):
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE, related_name='tournamentgroupteams_group', verbose_name="Group")
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='tournamentgroupteams_team', verbose_name="Team")
    hcp = models.IntegerField(null=True, blank=True, verbose_name="HCP")
    played = models.IntegerField(default=0, verbose_name="Played")
    win = models.IntegerField(default=0, verbose_name="Win")
    loss = models.IntegerField(default=0, verbose_name="Win")
    goal_scored = models.FloatField(default=0, verbose_name="Goal Scored")
    goal_conceded = models.FloatField(default=0, verbose_name="Goal Conceded")
    point_total = models.FloatField(default=0, verbose_name="Ppoint Total")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.group.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

class MatchType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class ChukkerChoice(models.Model):
    name = models.CharField(max_length=100)
    is_final = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name


class Matches(models.Model):
    class Status(models.TextChoices):
        UPCOMING = 'upcoming', 'Upcoming'
        LIVE = 'live', 'Live'
        FULLTIME = 'full-time', 'Full-Time'
        POSTPONED = 'postponed', 'Postponed'
        CANCELED = 'canceled', 'Canceled'
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Start Date")
    home_team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True, blank=True, related_name='home_team', verbose_name="Home Team")
    away_team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True, blank=True, related_name='away_team', verbose_name="Away Team")
    home_team_coach = models.ForeignKey(MatchCoach, on_delete=models.SET_NULL, null=True, blank=True, related_name='home_team_coaches', verbose_name="Home Team Coach")
    away_team_coach = models.ForeignKey(MatchCoach, on_delete=models.SET_NULL, null=True, blank=True, related_name='away_team_coaches', verbose_name="Away Team Coach")
    home_team_score = models.FloatField(verbose_name="Home Score", default=0)
    away_team_score = models.FloatField(verbose_name="Away Score", default=0)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE, related_name='tournament')
    venue = models.ForeignKey(Venues, on_delete=models.SET_NULL, null=True, blank=True, related_name='venue')
    status = models.CharField(max_length=150, null=True,  choices=Status.choices)
    chukkers = models.IntegerField(default=0)
    current_chukker = models.CharField(default=0, max_length=25, verbose_name="Current Chukker")
    final_chukkers = models.ManyToManyField(ChukkerChoice, blank=True, verbose_name="Final Chukkers", limit_choices_to={"is_final": True})
    referees = models.ManyToManyField(MatchReferees, blank=True, verbose_name="Referees")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    winner = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, blank=True,related_name='match_winner_team')
    tournament_only = models.BooleanField(default=False, verbose_name="Tournament Only")
    is_clickable =  models.BooleanField(default=True, verbose_name="Is Clickable")
    show_chukker =  models.BooleanField(default=True, verbose_name="Show chukker")
    show_matches =  models.BooleanField(default=True, verbose_name="Show in matches")
    show_voting =  models.BooleanField(default=False, verbose_name="Show Voting")
    class Voting(models.TextChoices):
        OPENED = 'opened', 'Opened'
        CLOSED = 'closed', 'Closed'
    voting =  models.CharField(max_length=150, null=True, default='opened', choices=Voting.choices, verbose_name="Voting")
    horse_only =  models.BooleanField(default=False, verbose_name="Horse Only")
    teams = models.ManyToManyField(Teams, blank=True, related_name='match_teams', verbose_name="Teams")


    def __str__(self) -> str:
        if self.tournament_only == True:
            return self.tournament.name
        else:
            home_team = self.home_team.name if self.home_team else "TBA"
            away_team = self.away_team.name if self.away_team else "TBA"
            return f"{home_team} vs {away_team}"



    def clean(self):
        # Call the parent class's clean method to ensure default cleaning
        super().clean()

        # Validate that home_team and away_team are not the same
        if self.home_team and self.away_team and self.home_team == self.away_team:
            raise ValidationError("The home team and away team cannot be the same.")

    def save(self, *args, **kwargs):
        # Call clean before saving
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
