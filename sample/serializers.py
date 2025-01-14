from rest_framework import serializers
from django_socio_grpc import proto_serializers
from rest_framework.exceptions import ValidationError
from sample.models import Matches
from sample.grpc.sample_pb2 import (
    MatchesRetrieveResponse,
    MatchesListResponse
)

class MatchesRetriveProtoSerializer(proto_serializers.ModelProtoSerializer):

    class Meta:
        model = Matches
        fields = (
            'id',
        )
        proto_class = MatchesRetrieveResponse
        proto_class_list = MatchesListResponse

