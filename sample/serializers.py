from rest_framework import serializers
from django_socio_grpc import proto_serializers
from rest_framework.exceptions import ValidationError
from sample.models import (
    Matches,
    Teams,
    Tournaments
)
from sample.grpc.sample_pb2 import (
    MatchesRetrieveResponse,
    MatchesListResponse
)

class MatchTournamentGrpcSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Tournaments
        fields = ['id', 'name', 'logo']

    def get_name(self, instance) -> str:
        return instance.name
    
class MatchTeamGrpcSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Teams
        fields = ['id', 'name', 'logo']

    def get_name(self, instance) -> str:
        return instance.name
    
class MatchesRetriveProtoSerializer(proto_serializers.ModelProtoSerializer):
    title = serializers.SerializerMethodField()
    tournament = MatchTournamentGrpcSerializer()
    home_team = MatchTeamGrpcSerializer()
    away_team = MatchTeamGrpcSerializer()
    home_team_score = serializers.SerializerMethodField()
    away_team_score = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Matches
        fields = (
            'id',
            'title',
            'tournament',
            'home_team',
            'away_team',
            'home_team_score',
            'away_team_score',
            'status',
        )
        proto_class = MatchesRetrieveResponse
        proto_class_list = MatchesListResponse
    
    def get_title(self, instance) -> str:
        home_team_title = ""
        away_team_title = ""
        title = ""
        home_team_title = instance.home_team
        away_team_title = instance.away_team

        if home_team_title !="" and away_team_title != "":
            title = f"{home_team_title} vs {away_team_title}"
        return title or home_team_title or away_team_title

    def get_home_team_score(self, instance) -> str:
        score = instance.home_team_score
        if score.is_integer():
            score = int(score)
        return str(score)
    
    def get_away_team_score(self, instance) -> str:
        score = instance.away_team_score
        if score.is_integer():
            score = int(score)
        return str(score)
    
    
    def get_status(self, instance) -> str:
        if instance.status:
            return instance.status
        return ""

