from django_socio_grpc import generics, mixins
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from sample.models import (
    Matches
)
from sample.serializers import (
    MatchesRetriveProtoSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.GRPC_PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

class MatchesService(mixins.AsyncListModelMixin, mixins.AsyncRetrieveModelMixin, generics.GenericService):
    permission_classes = [AllowAny]
    queryset = Matches.objects.all()
    serializer_class = MatchesRetriveProtoSerializer
    pagination_class = StandardResultsSetPagination