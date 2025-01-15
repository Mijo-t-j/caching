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
from django_socio_grpc.decorators import cache_endpoint, grpc_action, cache_endpoint_with_deleter, vary_on_metadata
from django.db.models.signals import post_save, post_delete
from asgiref.sync import sync_to_async
from django.core.cache import caches


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


    @cache_endpoint_with_deleter(300,
                                 cache="redis",
                                 key_prefix="match-retrieve",
                                 senders=(Matches,),
                                 invalidator_signals=(post_save, post_delete))
    async def Retrieve(self, request, context):
        self.serializer_class = MatchesRetriveProtoSerializer
        return await super(MatchesService, self).Retrieve(request, context)

    # def List(self, request, context):
    #     return super(MatchesService, self).List(request, context)


    # @grpc_action(
    #     request=[],
    #     response=MatchesRetriveProtoSerializer,
    #     use_generation_plugins=[
    #         ListGenerationPlugin(response=True),
    #     ],
    # )

    @cache_endpoint(300,cache="redis",key_prefix="match-list")
    @vary_on_metadata("lang")
    async def List(self, request, context):
        horse_matches = await sync_to_async(self.get_nothing)(caches)
        return await super().List(request, context)

    def get_nothing(self, caches):
        cache_instance = caches['redis']
        # delete_pattern = cache_instance.clear()
        # print(f"delete_pattern: {delete_pattern}")
        # print(f"cache.keys: {cache_instance.keys('*')}")
        # print(f"caches: {cache_instance.__dict__}")
